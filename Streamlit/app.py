import streamlit as st 
import os 
import cv2
from Number_plate_recognition.OCR_recognition import predict
from Vehicle_speed_and_colour_detection.speed_detection_model.speed_detector import trackMultipleObjects

<<<<<<< HEAD
https://chat.openai.com/share/79d4ccf3-fc4d-4f35-aa3e-c174593ceb0a
=======
def main():
    
    st.title("OCR Detection and Speed Detection App")
    
    st.write("Upload a video file to perform OCR recognition on Number Plate: ")
    uploaded_file1 = st.file_uploader("Choose a video file", type=["mp4","avi"])
    
    st.write("Upload a video file to detect speed: ")
    uploaded_file2 = st.file_uploader("Choose a video file", type=["mp4","avi"])
    
    
    
    
    
    

>>>>>>> ca2dea5ede67562362479b1513b87c124576b4e7
