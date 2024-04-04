import streamlit as st 
import sys
import os 
import cv2

from Vehicle_speed_and_colour_detection.speed_detection_model.speed_detector import trackMultipleObjects


def main():
    
    st.title("OCR Detection and Speed Detection App")
    
    options = ["Perform OCR recognition on Number Plate", "Detect speed"]
    selected_option = st.selectbox("Select an option:", options)

    uploaded_file = None

    video_path = st.text_input("Enter the path of the video file:")
    
    if st.button("Detect Speeding Vehicles"):
        if os.path.exists(video_path) and os.path.isfile(video_path):
            st.write("Processing...")
            trackMultipleObjects(video_path)
            st.write("Speed detection completed!")
        else:
            st.write("Please provide the path to the video file.")
        
    
if __name__ == "__main__":
    main()
