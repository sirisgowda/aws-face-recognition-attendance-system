"""
AWS Configuration File
----------------------
Stores all AWS-related configuration variables used by the
Face Recognition Attendance System.

Replace placeholder values with your own AWS resources
before deploying the application.
"""

# ==============================
# AWS REGION
# ==============================

AWS_REGION = "ap-south-1"

# ==============================
# AMAZON S3
# ==============================

S3_BUCKET = "student-attendance-bucket-mumbai"

REGISTERED_PREFIX = "registered/"
CAPTURED_PREFIX = "captured/"

# ==============================
# AMAZON REKOGNITION
# ==============================

REKOGNITION_COLLECTION = "student-faces"

SIMILARITY_THRESHOLD = 85.0

# ==============================
# DYNAMODB TABLES
# ==============================

EMPLOYEE_TABLE = "Employees"

ATTENDANCE_TABLE = "Attendance"

# ==============================
# AMAZON SNS
# ==============================

SNS_TOPIC_ARN = "arn:aws:sns:ap-south-1:YOUR_ACCOUNT_ID:student-attendance-alerts"

# ==============================
# GEOFENCING
# ==============================

# VIT Vellore Coordinates

VIT_LATITUDE = 12.9710
VIT_LONGITUDE = 79.1591

# Radius in meters

ALLOWED_RADIUS = 500

# ==============================
# CAMERA
# ==============================

CAMERA_INDEX = 0

# ==============================
# LIVENESS DETECTION
# ==============================

REQUIRED_BLINKS = 2

LIVENESS_TIMEOUT = 10