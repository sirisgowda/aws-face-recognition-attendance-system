import cv2
import time
import os

# -------------------------------
# Face & Eye Detection
# -------------------------------

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

eye_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_eye.xml"
)

# -------------------------------
# Capture Image
# -------------------------------

def capture_image(prompt="Press 's' to capture image"):

    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        raise RuntimeError("Camera not available")

    print(prompt)

    filename = f"{int(time.time())}.jpg"

    while True:

        ret, frame = cap.read()

        if not ret:
            continue

        cv2.putText(
            frame,
            prompt,
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2
        )

        cv2.imshow("Camera", frame)

        key = cv2.waitKey(1) & 0xFF

        if key == ord("s"):
            cv2.imwrite(filename, frame)
            break

        elif key == ord("q"):
            filename = None
            break

    cap.release()
    cv2.destroyAllWindows()

    return filename


# -------------------------------
# Simple Liveness Check
# -------------------------------

def simple_liveness_check(timeout=10, required_blinks=2):

    cap = cv2.VideoCapture(0)

    start = time.time()
    blink_count = 0
    previous_open = True

    print("Blink twice for liveness verification...")

    while time.time() - start < timeout:

        ret, frame = cap.read()

        if not ret:
            continue

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:

            roi = gray[y:y+h, x:x+w]

            eyes = eye_cascade.detectMultiScale(roi)

            eyes_open = len(eyes) >= 2

            if previous_open and not eyes_open:
                blink_count += 1

            previous_open = eyes_open

            cv2.rectangle(frame, (x, y), (x+w, y+h), (0,255,0), 2)

        cv2.imshow("Liveness Check", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

        if blink_count >= required_blinks:
            break

    cap.release()
    cv2.destroyAllWindows()

    return blink_count >= required_blinks