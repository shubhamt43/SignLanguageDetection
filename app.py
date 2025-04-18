from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import torch
from PIL import Image
import io
import pathlib
import sys



app = Flask(__name__)
CORS(app)

if sys.platform == "win32":
    pathlib.PosixPath = pathlib.WindowsPath
# Load model
model = torch.hub.load('ultralytics/yolov5', 'custom', path='yt.pt', force_reload=True)
model.conf = 0.8

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/detect', methods=['POST'])
def detect():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400

    image_file = request.files['image']
    image = Image.open(image_file.stream).convert('RGB')
    results = model(image)
    detections = results.pandas().xyxy[0]

    if detections.empty:
        return jsonify({'gesture': 'No gesture detected', 'confidence': 0.0}), 200

    top = detections.iloc[0]
    gesture = top['name']
    confidence = float(top['confidence'])

    return jsonify({'gesture': gesture, 'confidence': confidence}), 200

if __name__ == '__main__':
    app.run(debug=True)
