import streamlit as st 
import os 
import cv2
from Number_plate_recognition.OCR_recognition import predict
from Vehicle_speed_and_colour_detection.speed_detection_model.speed_detector import trackMultipleObjects

def main():
    
    st.title("OCR Detection and Speed Detection App")
    
    options = ["Perform OCR recognition on Number Plate", "Detect speed"]
    selected_option = st.selectbox("Select an option:", options)

    uploaded_file = None

    if selected_option == "Perform OCR recognition on Number Plate":
          predict()
    elif selected_option == "Detect speed":
        st.write("Upload a video file to detect speed:")
        uploaded_file = st.file_uploader("Choose a video file", type=["mp4", "avi"])

        trackMultipleObjects(uploaded_file, model_path="path_to_your_speed_model.pt")
        
    

