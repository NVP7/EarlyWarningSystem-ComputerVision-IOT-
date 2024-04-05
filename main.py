import math
import os
import time
from datetime import datetime
import pyrebase
import cvzone
from flask import Flask, render_template, Response
import threading
import cv2
from ultralytics import YOLO
from pyngrok import ngrok


app = Flask(__name__)
port_number = 5000
ngrok.set_auth_token("2eJpdeguUbV51Ni5eQ5LOQy4DA0_71Lwt7RhUNGQWzBSXdLzG")
public_url = ngrok.connect(port_number).public_url
config = {
    "apiKey": "AIzaSyD0WRvUV6s3Ybq-SeUF7_Sl3vZnWxKCSCE",
    "authDomain": "fire-protection-system-86468.firebaseapp.com",
    "databaseURL": "https://fire-protection-system-86468-default-rtdb.asia-southeast1.firebasedatabase.app",
    "projectId": "fire-protection-system-86468",
    "storageBucket": "fire-protection-system-86468.appspot.com",
    "messagingSenderId": "18331323194",
    "appId": "1:18331323194:web:9d66f6a38095569f9e9e03",
    "serviceAccount": "serviceAccount.json",
}
firebase = pyrebase.initialize_app(config)
storage = firebase.storage()
db = firebase.database()
db.child("CAMERA").update({"LiveStream": public_url})

capture = cv2.VideoCapture(0)
capture1 = cv2.VideoCapture(2)

@app.route("/")
def index():
    return render_template("index.html")
print(f"Bấm vào đây để truy cập:{public_url}")
def read_from_webcam():
    while True:
        ret, frame = capture.read()  # Sử dụng biến chia sẻ để đọc khung hình từ camera
        font = cv2.FONT_HERSHEY_SIMPLEX
        org = (50, 50)
        fontScale = 1
        color = (255, 0, 0)
        thickness = 2
        frame = cv2.putText(frame, datetime.now().strftime("%H:%M:%S"), org, font,
                          fontScale, color, thickness, cv2.LINE_AA)
        if ret:
            frame = cv2.resize(frame, (640, 480))
            _, image = cv2.imencode('.jpg', frame)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + image.tobytes() + b'\r\n')
def read_from_webcam1():
    while True:
        ret, frame = capture1.read()  # Sử dụng biến chia sẻ để đọc khung hình từ camera
        font = cv2.FONT_HERSHEY_SIMPLEX
        org = (50, 50)
        fontScale = 1
        color = (255, 0, 0)
        thickness = 2
        frame = cv2.putText(frame, datetime.now().strftime("%H:%M:%S"), org, font,
                            fontScale, color, thickness, cv2.LINE_AA)
        if ret:
            frame = cv2.resize(frame, (640, 480))
            _, image = cv2.imencode('.jpg', frame)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + image.tobytes() + b'\r\n')
@app.route("/image_feed")
def image_feed():
    return Response(read_from_webcam(), mimetype="multipart/x-mixed-replace; boundary=frame")
@app.route("/image_feed1")
def image_feed1():
    return Response(read_from_webcam1(), mimetype="multipart/x-mixed-replace; boundary=frame")
def run_flask_app():
    app.run(port=port_number)
def reset_flag_cam1():
    db.child("CAMERA").update({"CAM1": False})
def reset_flag_cam2():
    db.child("CAMERA").update({"CAM2": False})
def run_camera():
    model = YOLO('best.pt')
    classnames = [ 'Fire', 'Smoke', 'Cigarette','Spark']
    while True:
        ret, frame = capture.read()  # Sử dụng biến chia sẻ để đọc khung hình từ camera
        if ret:
            frame = cv2.resize(frame, (640, 480))
            result = model(frame, stream=True)
            for info in result:
                boxes = info.boxes
                for box in boxes:
                    confidence = box.conf[0]
                    confidence = math.ceil(confidence * 100)
                    Class = int(box.cls[0])
                    if confidence > 50:
                        db.child("CAMERA").update({"CAM1": True})
                        threading.Timer(30.0, reset_flag_cam1).start()
                        x1, y1, x2, y2 = box.xyxy[0]
                        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 5)
                        cvzone.putTextRect(frame, f'{classnames[Class]} {confidence}%', [x1 + 8, y1 - 10],
                                           scale=1.5, thickness=2)

                        current_day = time.strftime("%Y-%b-%d")
                        folder_path = os.path.join("History\Camera1",current_day)
                        if not os.path.exists(folder_path):
                            os.makedirs(folder_path)
                        filename = os.path.join(folder_path, str(time.strftime("%Y-%b-%d at %H.%M.%S %p")) + '.png')
                        cv2.imwrite(filename, frame)
                        print('Image saved as:', filename)
        cv2.imshow('CAM1', frame)
        key = cv2.waitKey(1)

def run_camera1():
    model = YOLO('best.pt')
    classnames = [ 'Fire', 'Smoke', 'Cigarette','Spark']
    while True:
        ret, frame = capture1.read()  # Sử dụng biến chia sẻ để đọc khung hình từ camera
        if ret:
            frame = cv2.resize(frame, (640, 480))
            result = model(frame, stream=True, device=0)
            for info in result:
                boxes = info.boxes
                for box in boxes:
                    confidence = box.conf[0]
                    confidence = math.ceil(confidence * 100)
                    Class = int(box.cls[0])
                    if confidence > 50:
                        db.child("CAMERA").update({"CAM2": True})
                        threading.Timer(30.0, reset_flag_cam2).start()
                        x1, y1, x2, y2 = box.xyxy[0]
                        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 5)
                        cvzone.putTextRect(frame, f'{classnames[Class]} {confidence}%', [x1 + 8, y1 - 10],
                                           scale=1.5, thickness=2)

                        current_day = time.strftime("%Y-%b-%d")
                        folder_path = os.path.join("History\Camera2", current_day)
                        if not os.path.exists(folder_path):
                            os.makedirs(folder_path)
                        filename = os.path.join(folder_path, str(time.strftime("%Y-%b-%d at %H.%M.%S %p")) + '.png')
                        cv2.imwrite(filename, frame)
                        print('Image saved as:', filename)
        cv2.imshow('CAM2', frame)
        key = cv2.waitKey(1)
def FireBase():
    current_day = time.strftime("%Y-%b-%d")
    folder_path = os.path.join("History\Camera1", current_day)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    while True:
        file_names = os.listdir(folder_path)
        for file_name in file_names:
            file_path = os.path.join(folder_path, file_name)
            storage = firebase.storage()
            destination_path = "Camera1/" + current_day + "/" + os.path.basename(file_name)
            storage.child(destination_path).put(file_path)
            print(f"Uploaded {file_name} to {file_path} in Firebase Storage")
            os.remove(file_path)  # Sau khi tải lên xóa các tập tin đã lưu trong máy
def FireBase1():
    current_day = time.strftime("%Y-%b-%d")
    folder_path = os.path.join("History\Camera2", current_day)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    while True:
        file_names = os.listdir(folder_path)
        for file_name in file_names:
            file_path = os.path.join(folder_path, file_name)
            storage = firebase.storage()
            destination_path = "Camera2/" + current_day + "/" + os.path.basename(file_name)
            storage.child(destination_path).put(file_path)
            print(f"Uploaded {file_name} to {file_path} in Firebase Storage")
            os.remove(file_path)  # Sau khi tải lên xóa các tập tin đã lưu trong máy
def start_app():
    flask_thread = threading.Thread(target=run_flask_app)
    camera_thread = threading.Thread(target=run_camera)
    camera1_thread = threading.Thread(target=run_camera1)
    FireBaseCam = threading.Thread(target=FireBase)
    FireBaseCam1 = threading.Thread(target=FireBase1)
    FireBaseCam.start()
    FireBaseCam1.start()
    flask_thread.start()
    camera_thread.start()
    camera1_thread.start()

if __name__ == "__main__":
    start_app()

