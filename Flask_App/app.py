from flask import Flask, request , render_template
import cv2
import numpy as np
import joblib

import requests

app = Flask(__name__)

vehicle_detection_api = "http://"
enhanced_video_api = " "
number_plate_detection_api = " "
anomally_detection_api = ""

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/procss_video', methods = ['POST'])
def process_video():
    video_file = requests.files['video']

    video_bytes -
    #get the uploaded video file





@app.route('/process_video', methods=['POST'])
def process_video():
    video_file = request.files['video']

    video_bytes = video_file.read()


results = {
    'vehicle_detection' : vehicle_detection,
     'anomaly_frames' : anomaly_frames
    'number_plate_detection' : number_plate_detection_api
}

#render the result template with the processed results
return render_template('result.html', results = results)

if __name__ = '__main__':
    app.run(debug = True)


