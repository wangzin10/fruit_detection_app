from flask import Flask, render_template, request, send_file
from ultralytics import YOLO
import cv2
import numpy as np
import os
from PIL import Image
from time import time
import io

app = Flask(__name__)

model = YOLO("D:/HK_personal project/project_2_FruitDetection/model/best.pt")  

@app.route('/')
def index():
    return render_template("web.html")

@app.route('/detect', methods=['POST'])
def detect():
    file = request.files['image']
    image = Image.open(file.stream).convert("RGB")
    image_np = np.array(image)

    results = model(image_np)[0]

    # Vẽ box
    for box in results.boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        conf = float(box.conf)
        label = int(box.cls)
        class_name = model.names[label]

        cv2.rectangle(image_np, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(image_np, f"{class_name} {conf:.2f}", (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    # Lưu ảnh kết quả
    result_path = "static/result.jpg"
    Image.fromarray(image_np).save(result_path)

    return {
        "result_url": f"/static/result.jpg?timestamp={int(time())}"
    }
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
