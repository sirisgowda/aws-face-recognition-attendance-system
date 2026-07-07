# AWS Face Recognition Attendance System

## Overview

The **AWS Face Recognition Attendance System** is a cloud-based attendance management application that automates employee attendance using facial recognition. The system integrates multiple AWS services to provide secure identity verification, attendance tracking, geo-fencing validation, emotion detection, and real-time alert notifications.

The application captures images through a webcam, verifies identities using Amazon Rekognition, stores employee and attendance data in Amazon DynamoDB, saves images in Amazon S3, and sends email alerts through Amazon SNS for unauthorized access attempts.

---

# Features

- Face-based employee registration
- Real-time face recognition
- Automated attendance marking
- Emotion detection using Amazon Rekognition
- Geo-fencing validation
- Duplicate attendance prevention
- Unknown face detection
- Email alerts using Amazon SNS
- Cloud-based attendance storage
- Attendance report generation

---

# AWS Services Used

- Amazon Rekognition
- Amazon S3
- Amazon DynamoDB
- Amazon SNS
- AWS Lambda
- Boto3 SDK

---

# Technology Stack

## Programming Language

- Python

## Cloud Services

- Amazon Rekognition
- Amazon S3
- Amazon DynamoDB
- Amazon SNS
- AWS Lambda

## Computer Vision

- OpenCV
- Haar Cascade Classifiers

## Libraries

- boto3
- requests
- pandas
- numpy

---

# System Workflow

```
Webcam
   │
   ▼
Capture Image
   │
   ▼
Liveness Check
   │
   ▼
Upload Image to Amazon S3
   │
   ▼
Amazon Rekognition Face Search
   │
   ▼
Employee Verification
   │
   ├────────► Unknown Face
   │              │
   │              ▼
   │         Amazon SNS Alert
   │
   ▼
Geo-fencing Validation
   │
   ▼
Emotion Detection
   │
   ▼
Attendance Stored in DynamoDB
```

---

# Project Structure

```
aws-face-recognition-attendance-system/

│
├── backend/
│   ├── attendance_system.py
│   ├── aws_config.py
│   ├── utils.py
│   └── requirements.txt
│
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
│
├── lambda/
│   ├── get_attendance.py
│   ├── get_employees.py
│   └── register_employee.py
│
├── screenshots/
│
├── README.md
├── LICENSE
└── .gitignore
```

---

# Installation

Clone the repository

```bash
git clone https://github.com/sirisgowda/aws-face-recognition-attendance-system.git

cd aws-face-recognition-attendance-system
```

Install dependencies

```bash
pip install -r backend/requirements.txt
```

Run the application

```bash
python backend/attendance_system.py
```

---

# Screenshots

## Amazon S3 Bucket

![Amazon S3](screenshots/amazons3.png)

---

## Registered Objects in S3

![Objects Registered](screenshots/objects%20reg.png)

---

## Captured Objects in S3

![Objects](screenshots/objects.png)

---

## Amazon DynamoDB

![AmazonDB](screenshots/amazondb.png)

---

## Employee Table

![Employee Table](screenshots/emp%20table.png)

---

## Attendance Table

![Attendance Table](screenshots/attendance%20table.png)

---

## Register an Employee

![Register Employee](screenshots/register%20an%20employee.png)

---

## Captured Image

![Captured Image](screenshots/image%20captured.png)

---

## Attendance First Attempt

![Attendance First Attempt](screenshots/attendance%20first%20attempt.png)

---

## Duplicate Attendance

![Duplicate Attendance](screenshots/duplicate%20attendance.png)

---

## Geo Fencing

![Geo Fencing](screenshots/geo%20fencing%20(1).png)

---

## Geo Fencing Alert

![Geo Fencing Alert](screenshots/geo%20fencing%20(2).png)

---

## Unknown Face Detection

![Unknown Face](screenshots/unknown%20face%20detected(unregistered).png)


# Demo Video

A walkthrough of the project implementation and attendance workflow:

- 🎥 Part 1: https://www.loom.com/share/dfeec5f74e984d71b1141cc8dc4c969b
- 🎥 Part 2: https://www.loom.com/share/a6c63367173240b0874b0f8f397cbd39
---

# My Contribution

- Designed and implemented the backend attendance workflow.
- Integrated Amazon Rekognition for face recognition and emotion detection.
- Connected Amazon S3 for image storage.
- Integrated Amazon DynamoDB for employee and attendance records.
- Implemented geo-fencing validation.
- Added duplicate attendance prevention.
- Integrated Amazon SNS for automated email alerts.
- Built AWS Lambda functions for cloud-based operations.
- Developed and tested the complete cloud workflow.

---

# Future Improvements

- Multi-face attendance support
- Mobile application integration
- Real-time analytics dashboard
- Face mask detection
- Role-based authentication
- Cloud deployment using API Gateway and EC2

---

# License

This project was developed for educational purposes to demonstrate cloud-native attendance management using AWS services.
