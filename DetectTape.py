#!/usr/bin/env python3

import cv2
import visionpipeline as render
import CameraUtilities
import numpy as np
from networktables import NetworkTables

def Distance_To_Camera(knownWidth, focalLength, perWidth):
    # compute and return the distance from the maker to the camera
    return (knownWidth * focalLength) / perWidth

KNOWN_DISTANCE = 24.0
KNOWN_WIDTH = 11.0
FOCAL_LENGTH = (300 * KNOWN_DISTANCE) / KNOWN_WIDTH
HEIGHT = 11.5
FOV = 35

cap = cv2.VideoCapture(1)
pipeline = render.GripPipeline()

running = NetworkTables.initialize(server='10.17.26.2')
if(running):
    print("Running")
preferences = NetworkTables.getTable("Preferences")

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    #grab networktable values
    h_lower = preferences.getNumber("Vision/H/Lower", 3)
    h_upper = preferences.getNumber("Vision/H/Upper", 46)
    s_lower = preferences.getNumber("Vision/S/Lower", 0)
    s_upper = preferences.getNumber("Vision/S/Upper", 255)
    l_lower = preferences.getNumber("Vision/L/Lower", 179)
    l_upper = preferences.getNumber("Vision/L/Upper", 255)

    # Change base values
    hue = [h_lower, h_upper]
    saturation = [s_lower, s_upper]
    luminance = [l_lower, l_upper]

    pipeline.setHSL(hue, saturation, luminance)

    # Our operations on the frame come here
    pipeline.process(frame)
    output = pipeline.hsl_threshold_output

    #gets the contours
    contours = pipeline.filter_contours_output

    rects = []
    boxes = []
    contours = []
    for contour in contours:
        rect = cv2.minAreaRect(contour)
        box = cv2.boxPoints(rect)
        box = np.int0(box)

        rects.append(rect)
        boxes.append(box)

    screenHeight = frame.shape[0]

    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        bottom = screenHeight - (y + h)
        print(y)
        print(h)
        print(x)
        print(w)
        print(bottom)
        print(CameraUtilities.FloorDistance(y+h, screenHeight, FOV, HEIGHT))
        cv2.rectangle(frame, (x,y), (x+w, y+h), (255,0,0))

    distances = []
    for rect in rects:
 #       y_center = rect[0][1]
 #       height = rect[1][1]
 #       bottom = screenHeight-(y_center - (height/2))
 #       print(y_center)
 #       print(height)
 #       print(bottom)
 #       print(CameraUtilities.FloorDistance(bottom, screenHeight, FOV, HEIGHT))
        distances.append(Distance_To_Camera(KNOWN_WIDTH, FOCAL_LENGTH, rect[1][0]))

    # Display the resulting frame
    cv2.drawContours(frame, contours, 0, (0,255,0), 2)
    cv2.drawContours(frame, boxes, 0, (0,0,255), 2)

#    for distance in distances:
#        print(distance)

    cv2.imshow('input', frame)
    if cv2.waitKey(60) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv.GetSize(src)