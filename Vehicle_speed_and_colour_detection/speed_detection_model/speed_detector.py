# Importing Libraries
import numpy as np
import cv2
import dlib
# run the command 
""" python -m pip install dlib-19.22.99-cp310-cp310-win_amd64.whl
"""
import time
import math
import csv
import os

# Classifier File
carCascade = cv2.CascadeClassifier("vech.xml")

# Video file capture
video = cv2.VideoCapture("carsVideo.mp4")

# Constant Declaration
WIDTH = 1280
HEIGHT = 720

# CSV Reader Func
color_ranges = {}
with open("colors.csv", mode = 'r') as file:
    reader = csv.reader(file)

    for row in reader:
        color_ranges[row[1]] = [row[3], row[4], row[5]]

newpath = 'speeding_vehicles' 
if not os.path.exists(newpath):
    os.makedirs(newpath)


# Function to detect color of car
def detect_car_color(image, x, y, w, h):
    # Convert the region of interest to HSV color space
    roi = image[y:y+h, x:x+w]
    A = cv2.mean(roi)
    #print(A)
    a_r = A[0] if(A[0] != np.NaN) else 0
    a_g = A[1] if(A[2] != np.NaN) else 0
    a_b = A[2] if(A[2] != np.NaN) else 0

    # Check color presence in the region of interest
    min_dist = 10000;
    for color, [r, g, b] in color_ranges.items():
        dist = abs(int(r) - int(a_r)) + abs(int(b)  - int(a_b)) + abs(int(g)  - int(a_g))
        if dist < min_dist:
            min_dist = dist
            req_color = color

    return req_color


# estimate speed function
def estimateSpeed(location1, location2):
    d_pixels = math.sqrt(math.pow(location2[0] - location1[0], 2) + math.pow(location2[1] - location1[1], 2))
    ppm = 8.8
    d_meters = d_pixels / ppm
    fps = 18
    speed = d_meters * fps * 3.6
    return speed


# tracking multiple objects
def trackMultipleObjects():
    s_id = 0
    rectangleColor = (0, 255, 255)
    #rectangleColor2 = (255, 0, 0)
    frameCounter = 0
    currentCarID = 0
    fps = 0
    PADDING = 100

    carTracker = {}
    carNumbers = {}
    carLocation1 = {}
    carLocation2 = {}
    car_id_exists = []
    speed = [None] * 1000

    #out = cv2.VideoWriter('outTraffic.mp4', cv2.VideoWriter_fourcc(*'mp4v'), 10, (WIDTH, HEIGHT))

    while True:
        start_time = time.time()
        rc, image = video.read()
        if type(image) == type(None):
            break

        image = cv2.resize(image, (WIDTH, HEIGHT))
        resultImage = image.copy()

        frameCounter = frameCounter + 1
        carIDtoDelete = []

        for carID in carTracker.keys():
            trackingQuality = carTracker[carID].update(image)

            if trackingQuality < 7:
                carIDtoDelete.append(carID)

        for carID in carIDtoDelete:
            print("Removing carID " + str(carID) + ' from list of trackers. ')
            print("Removing carID " + str(carID) + ' previous location. ')
            print("Removing carID " + str(carID) + ' current location. ')
            carTracker.pop(carID, None)
            carLocation1.pop(carID, None)
            carLocation2.pop(carID, None)

        if not (frameCounter % 10):
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            cars = carCascade.detectMultiScale(gray, 1.1, 13, 18, (24, 24))

            for (_x, _y, _w, _h) in cars:
                x = int(_x)
                y = int(_y)
                w = int(_w)
                h = int(_h)

                x_bar = x + 0.5 * w
                y_bar = y + 0.5 * h

                matchCarID = None

                for carID in carTracker.keys():
                    trackedPosition = carTracker[carID].get_position()

                    t_x = int(trackedPosition.left())
                    t_y = int(trackedPosition.top())
                    t_w = int(trackedPosition.width())
                    t_h = int(trackedPosition.height())

                    t_x_bar = t_x + 0.5 * t_w
                    t_y_bar = t_y + 0.5 * t_h

                    if ((t_x <= x_bar <= (t_x + t_w)) and (t_y <= y_bar <= (t_y + t_h)) and (
                            x <= t_x_bar <= (x + w)) and (y <= t_y_bar <= (y + h))):
                        matchCarID = carID

                if matchCarID is None:
                    print(' Creating new tracker' + str(currentCarID))

                    tracker = dlib.correlation_tracker()
                    tracker.start_track(image, dlib.rectangle(x, y, x + w, y + h))

                    carTracker[currentCarID] = tracker
                    carLocation1[currentCarID] = [x, y, w, h]

                    currentCarID = currentCarID + 1

        for carID in carTracker.keys():
            trackedPosition = carTracker[carID].get_position()

            t_x = int(trackedPosition.left())
            t_y = int(trackedPosition.top())
            t_w = int(trackedPosition.width())
            t_h = int(trackedPosition.height())
            
            # Increased the box size
            ## Uncomment for better understanding
            #cv2.rectangle(resultImage, (t_x - 10, t_y - 10), (t_x + t_w + 20, t_y + t_h + 20), rectangleColor, 4)
            #cv2.rectangle(resultImage, (t_x, t_y), (t_x + t_w , t_y + t_h ), rectangleColor2, 4)

            carLocation2[carID] = [t_x, t_y, t_w, t_h]

        end_time = time.time()

        if not (end_time == start_time):
            fps = 1.0 / (end_time - start_time)

        for i in carLocation1.keys():
            if frameCounter % 1 == 0:
                [x1, y1, w1, h1] = carLocation1[i]
                [x2, y2, w2, h2] = carLocation2[i]

                carLocation1[i] = [x2, y2, w2, h2]

                if [x1, y1, w1, h1] != [x2, y2, w2, h2]:
                    if (speed[i] == None or speed[i] == 0) and y1 >= 275 and y1 <= 285:
                        speed[i] = estimateSpeed([x1, y1, w1, h1], [x1, y2, w2, h2])
                        
                    car_color = detect_car_color(resultImage, x1, y1, w1, h1)
                    if car_color:
                        print("Car color:", car_color)
                        #cv2.putText(resultImage, " Color: " + car_color + "km/h", (int(x1 + w1 / 2), int(y1 - 5)), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 100), 2)

                        if speed[i] != None and y1 >= 280:
    
                            if speed[i] > 50:
                                if i not in car_id_exists:
                                    car_id_exists.append(i)
                                    s_id += 1
                                    pic = resultImage[y1 - PADDING : y1 + h1 + PADDING, x1 - PADDING : x1 + w1 + PADDING]
                                    cv2.imwrite(f"{newpath}\\sc_frame_{s_id}_{speed[i]:{2}.{4}}_{car_color}.jpg", pic)
                                    cv2.putText(resultImage, " Color: " + car_color + " : " + str(int(speed[i])) + "km/h", (int(x1 + w1 / 2), int(y1 - 5)), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 100), 2)
                            else:
                                cv2.putText(resultImage, " Color: " + car_color + " : " + str(int(speed[i])) + "km/h", (int(x1 + w1 / 2), int(y1 - 5)), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 100, 0), 2)
                            
                            #cv2.imwrite(f"speeding_car_frame_{snapshot_count}.jpg", resultImage)
                            
        cv2.imshow('result', resultImage)

        #out.write(resultImage)

        if cv2.waitKey(1) == 27:
            break

    cv2.destroyAllWindows()
    #out.release()


if __name__ == '__main__':
    trackMultipleObjects()
