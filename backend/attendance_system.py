import os
import cv2
import uuid
import boto3
import requests
import pandas as pd
import calendar
import sys

from datetime import datetime, timezone
from dateutil import parser
from boto3.dynamodb.conditions import Attr

from aws_config import *
from utils import *

# ==========================================
# AWS INITIALIZATION
# ==========================================

rekognition = boto3.client(
    "rekognition",
    region_name=AWS_REGION
)

dynamodb = boto3.resource(
    "dynamodb",
    region_name=AWS_REGION
)

employee_table = dynamodb.Table(EMPLOYEE_TABLE)

attendance_table = dynamodb.Table(ATTENDANCE_TABLE)

# ==========================================
# REGISTER FACE
# ==========================================

def register_face(local_path, name, email):

    # Check if employee already exists

    existing = employee_table.scan(

        FilterExpression=
        Attr("Name").eq(name) |
        Attr("Email").eq(email)

    )

    if existing["Items"]:

        print("Employee already registered.")

        return existing["Items"][0]["EmployeeID"]

    employee_id = str(uuid.uuid4())

    s3_key = REGISTERED_PREFIX + os.path.basename(local_path)

    upload_to_s3(local_path, s3_key)

    response = rekognition.index_faces(

        CollectionId=REKOGNITION_COLLECTION,

        Image={

            "S3Object": {

                "Bucket": S3_BUCKET,

                "Name": s3_key

            }

        },

        ExternalImageId=employee_id,

        DetectionAttributes=["ALL"]

    )

    if not response["FaceRecords"]:

        print("No face detected.")

        return None

    face_id = response["FaceRecords"][0]["Face"]["FaceId"]

    employee_table.put_item(

        Item={

            "EmployeeID": employee_id,

            "Name": name,

            "Email": email,

            "FaceID": face_id,

            "ImageKey": s3_key,

            "CreatedAt": datetime.utcnow().isoformat()

        }

    )

    print("Employee Registered Successfully")

    print("Employee ID :", employee_id)

    return employee_id
# ==========================================
# RECOGNIZE FACE
# ==========================================

def recognize_face(local_path):

    # -------------------------------
    # GEO VALIDATION
    # -------------------------------

    if not inside_vit():

        message = (
            "Attendance blocked.\n\n"
            "User attempted to mark attendance "
            "outside the allowed campus radius."
        )

        send_alert_email(message)

        print("Attendance blocked (Outside Campus).")

        return None

    print("Inside Campus")

    # -------------------------------
    # Upload captured image
    # -------------------------------

    s3_key = CAPTURED_PREFIX + os.path.basename(local_path)

    upload_to_s3(local_path, s3_key)

    # -------------------------------
    # Search face
    # -------------------------------

    response = rekognition.search_faces_by_image(

        CollectionId=REKOGNITION_COLLECTION,

        Image={
            "S3Object": {
                "Bucket": S3_BUCKET,
                "Name": s3_key
            }
        },

        MaxFaces=1,

        FaceMatchThreshold=SIMILARITY_THRESHOLD

    )

    # -------------------------------
    # Unknown Face
    # -------------------------------

    if not response.get("FaceMatches"):

        image_url = f"https://{S3_BUCKET}.s3.amazonaws.com/{s3_key}"

        message = (
            "Unknown face detected.\n\n"
            f"Timestamp : {datetime.utcnow().isoformat()}\n\n"
            f"Image : {image_url}"
        )

        send_alert_email(message)

        print("Unknown Face")

        return None

    # -------------------------------
    # Match Found
    # -------------------------------

    match = response["FaceMatches"][0]

    face_id = match["Face"]["FaceId"]

    similarity = match["Similarity"]

    # -------------------------------
    # Emotion Detection
    # -------------------------------

    emotion_response = rekognition.detect_faces(

        Image={
            "S3Object": {
                "Bucket": S3_BUCKET,
                "Name": s3_key
            }
        },

        Attributes=["ALL"]

    )

    emotion = "UNKNOWN"

    if emotion_response["FaceDetails"]:

        emotion = emotion_response["FaceDetails"][0]["Emotions"][0]["Type"]

    # -------------------------------
    # Find Employee
    # -------------------------------

    employee = employee_table.scan(

        FilterExpression=Attr("FaceID").eq(face_id)

    )

    if not employee["Items"]:

        print("Employee record not found.")

        return None

    employee = employee["Items"][0]

    employee_id = employee["EmployeeID"]

    name = employee["Name"]

    # -------------------------------
    # Duplicate Attendance Check
    # -------------------------------

    if already_marked_today(employee_id):

        print("Attendance already marked today.")

        return employee_id

    # -------------------------------
    # Save Attendance
    # -------------------------------

    attendance_id = str(uuid.uuid4())

    attendance_table.put_item(

        Item={

            "AttendanceID": attendance_id,

            "EmployeeID": employee_id,

            "Name": name,

            "Timestamp": datetime.utcnow().isoformat(),

            "ImageKey": s3_key,

            "Confidence": round(similarity, 2),

            "Emotion": emotion

        }

    )

    print("--------------------------------")

    print("Attendance Marked Successfully")

    print("Employee :", name)

    print("Similarity :", round(similarity, 2))

    print("Emotion :", emotion)

    print("--------------------------------")

    return employee_id
# ==========================================
# ATTENDANCE STATISTICS
# ==========================================

def attendance_stats(employee_id):

    now = datetime.utcnow()

    response = attendance_table.scan(

        FilterExpression=Attr("EmployeeID").eq(employee_id)

    )

    items = response.get("Items", [])

    present_days = set()

    for item in items:

        dt = parser.isoparse(item["Timestamp"])

        if dt.year == now.year and dt.month == now.month:

            present_days.add(dt.date())

    total_working_days = 0

    for day in range(
        1,
        calendar.monthrange(now.year, now.month)[1] + 1
    ):

        if datetime(now.year, now.month, day).weekday() < 5:

            total_working_days += 1

    attendance_percentage = 0

    if total_working_days != 0:

        attendance_percentage = (
            len(present_days) /
            total_working_days
        ) * 100

    print("\n========== ATTENDANCE ==========")
    print("Days Present :", len(present_days))
    print("Working Days :", total_working_days)
    print("Attendance % :", round(attendance_percentage, 2))
    print("================================\n")

    return attendance_percentage


# ==========================================
# REGISTER ACTION
# ==========================================

def action_register():

    if not simple_liveness_check():

        print("Liveness verification failed.")

        return

    image = capture_image(
        "Register : Press 'S' to Capture"
    )

    if image is None:
        return

    name = input("Enter Name : ")

    email = input("Enter Email : ")

    employee_id = register_face(
        image,
        name,
        email
    )

    if os.path.exists(image):
        os.remove(image)

    if employee_id:

        print("Employee ID :", employee_id)


# ==========================================
# RECOGNIZE ACTION
# ==========================================

def action_recognize():

    if not simple_liveness_check():

        print("Liveness verification failed.")

        return

    image = capture_image(
        "Recognize : Press 'S' to Capture"
    )

    if image is None:
        return

    employee_id = recognize_face(image)

    if employee_id:

        attendance_stats(employee_id)

    if os.path.exists(image):
        os.remove(image)


# ==========================================
# GENERATE CSV REPORT
# ==========================================

def action_report(employee_id):

    response = attendance_table.scan(

        FilterExpression=Attr("EmployeeID").eq(employee_id)

    )

    rows = []

    for item in response.get("Items", []):

        rows.append([

            item["Timestamp"],

            item["Name"],

            item["Confidence"],

            item["Emotion"]

        ])

    df = pd.DataFrame(

        rows,

        columns=[

            "Timestamp",

            "Name",

            "Confidence",

            "Emotion"

        ]

    )

    filename = f"attendance_report_{employee_id}.csv"

    df.to_csv(filename, index=False)

    print("Report Saved :", filename)


# ==========================================
# MAIN
# ==========================================

if __name__ == "__main__":

    if len(sys.argv) < 2:

        print("\nUsage:")

        print("python attendance_system.py register")

        print("python attendance_system.py recognize")

        print("python attendance_system.py report EMPLOYEE_ID")

        sys.exit()

    command = sys.argv[1].lower()

    if command == "register":

        action_register()

    elif command == "recognize":

        action_recognize()

    elif command == "report":

        if len(sys.argv) < 3:

            print("Employee ID required.")

        else:

            action_report(sys.argv[2])

    else:

        print("Invalid Command")