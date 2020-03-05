import inference
from flask import Flask, request, jsonify
import numpy as np
import base64
from PIL import Image
import pyrebase
from dotenv import load_dotenv
load_dotenv()
import os

import detect_ocr

app = Flask(__name__)
config = {
  "apiKey": os.getenv("apiKey"),
  "authDomain": os.getenv("authDomain"),
  "databaseURL": os.getenv("databaseURL"),
  "storageBucket": os.getenv("storageBucket"),
#   "serviceAccount": "park-o-report-firebase-adminsdk.json"
}
firebase = pyrebase.initialize_app(config)
db = firebase.database()
storage = firebase.storage()

@app.route("/api/number-plate/detect", methods=["POST"])
def detect():
    image = request.files.get("img")
    image = Image.open(image)

    image_np = np.array(image)
    output, out_image = inference.show_inference(image=image_np, image_draw=False)
    print(output)
    return jsonify(output)

@app.route("/api/number-plate/detectFromDB", methods=["POST"])
def detectFromDB():
    uuid = request.form.get("uuid")
    tmp_path = "tmp.jpg"
    tmp_crop_path = "tmp_cropped_{}.jpg"
    storage.child(f"images/{uuid}").download(tmp_path)
    report = db.child("reports").child(uuid).get().val()
    rect = report["rect"]
    print(rect)
    xmin = rect["x"]
    xmax = rect["x"] + rect["w"]
    ymin = rect["y"]
    ymax = rect["y"] + rect["h"]

    detect_ocr.crop_img(tmp_path, [(ymin, xmin, ymax, xmax)], tmp_crop_path)

    image_path=tmp_crop_path.format(1)
    boxes, image_np = detect_ocr.show_inference(image_path=image_path, image_draw=False)
    detect_ocr.crop_img(image_path, boxes)
    texts = detect_ocr.gcloud_ocr(os.getcwd())
    text = ""
    if len(texts) > 0:
        text = " ".join(texts)
        text = detect_ocr.process_image(text)

    if not text:
        text = detect_ocr.gcloud_ocr_whole_image(tmp_path)
        text = detect_ocr.process_image(text)

    print(text)

    return jsonify({"number": text})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)
