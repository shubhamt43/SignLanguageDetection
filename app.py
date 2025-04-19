from flask import Flask, request, jsonify, send_from_directory
import torch
import sys
from PIL import Image
from pathlib import Path
from flask_cors import CORS
import io

app = Flask(__name__)
CORS(app)
# Add YOLOv5 path
sys.path.append(str(Path(__file__).parent / "yolov5"))

# Import YOLOv5 model loader
from models.common import DetectMultiBackend

# Load model (path must match filename in your Space)
model = torch.hub.load('./yolov5', 'custom', path='yt.pt', source='local')
model.conf = 0.5


@app.route('/')
def home():
    return send_from_directory('templates', 'index.html')

@app.route('/makers')
def makers():
    return send_from_directory('templates', 'makers.html')

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
    app.run(host='0.0.0.0', port=7860)