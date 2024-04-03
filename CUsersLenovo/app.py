from flask import Flask, request, render_template, jsonify
import requests

app = Flask(__name__)

# URLs for the APIs hosting your models
vehicle_detection_api = "http://your_vehicle_detection_api_endpoint"
anomaly_detection_api = "http://your_anomaly_detection_api_endpoint"
number_plate_detection_api = "http://your_number_plate_detection_api_endpoint"


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/process_video', methods=['POST'])
def process_video():
    # Get the uploaded video file and car color
    video_file = request.files['video']
    color = request.form['color']

    # Send the video file to vehicle detection model API
    video_bytes = video_file.read()
    vehicle_detection_response = requests.post(vehicle_detection_api, files={'video': video_bytes})
    vehicle_detections = vehicle_detection_response.json()

    # Send the video file to anomaly detection model API
    anomaly_detection_response = requests.post(anomaly_detection_api, files={'video': video_bytes})
    anomaly_frames = anomaly_detection_response.json()

    # Process the frames to detect car color
    # Your code for processing frames and filtering cars of specified color goes here

    # Process only the frames with cars of specified color
    color_filtered_frames = []
    for frame in anomaly_frames:
    # Your code to filter cars of specified color and store the frames

    # Initialize list to store number plate detections
    number_plate_detections = []

    # Send each filtered frame to number plate detection model API
    for frame in color_filtered_frames:
        response = requests.post(number_plate_detection_api, files={'frame': frame})
        number_plate_detections.append(response.json())

    # Render the result template with the processed results
    return render_template('result.html', number_plate_detections=number_plate_detections)


if __name__ == '__main__':
    app.run(debug=True)
