import streamlit as st 
import os 
import cv2
from Number_plate_recognition.OCR_recognition import predict
from Vehicle_speed_and_colour_detection.speed_detection_model.speed_detector import trackMultipleObjects

https://chat.openai.com/share/79d4ccf3-fc4d-4f35-aa3e-c174593ceb0a