#!/usr/bin/env python3

import cv2
import numpy as np
import math
import time

class SimilarContours:


    def __init__(self, maxContours, timeout):
        self.__timeout = timeout
        self.__maxContours = maxContours
        self.__storedContours = []
        self.__TimeStamps = []

    def checkContours(self, contour):
        if not self.__storedContours:
            self.__storedContours.append(contour)
            return 0

        M_Input = cv2.moments(contour)
        M_Stored = cv2.moments(self.__storedContours[-1])

        X_Input = M_Input['m10']/M_Input['m00']
        Y_Input = M_Input['m01']/M_Input['m00']
        Area_Input = M_Input['m00']
        
        X_Stored = M_Stored['m10']/M_Stored['m00']
        Y_Stored = M_Stored['m01']/M_Stored['m00']
        Area_Stored = M_Stored['m00']


        Linear_Distance_Input = math.sqrt(X_Input**2 + Y_Input**2)
        Linear_Distance_Stored = math.sqrt(X_Stored**2 + Y_Stored**2)

        Area_Diff = (Area_Stored - Area_Input) / ((Area_Stored + Area_Input) / 2)
        Linear_Distance_diff = (Linear_Distance_Stored - Linear_Distance_Input) / ((Linear_Distance_Stored - Linear_Distance_Input) / 2)

        return checkContours

    def insertContours(self, contour):

        if len(self.__storedContours) >= self.__maxContours:
            self.__storedContours.pop(0)
            self.__CurrentTime.pop(0)
        
        CurrentTime = time.time()
        __TimeStamps.append(CurrentTime)

        self.__storedContours.append(self.__storedContours)


    def AverageValues(self):
        if not self.__storedContours
            return 0, 0, 0, 0

        SumOfX = 0
        SumOfY = 0
        SumOfWidth = 0
        SumOfHeight = 0
        
        for contour in self.__storedContours:
            x, y, w, h = cv2.boundingRect(contour)
            SumOfX = x + SumOFX
            SumOfY = Y + SumOfY
            SumOfWidth = x + SumOfWidth
            SumOfHeight = x + SumOfHeight

        List_Size = len(self.__storedContours)

        XAverage = SumOfX / List_Size
        YAverage = SumOfY / List_Size
        HeightAverage = SumOfHeight / List_Size
        WidthAverage = SumOfWidth / List_Size
     
        return XAverage, YAverage, WidthAverage, HeightAverage

    def removeOld(self):
        currentTime = time.time()
        while currentTime - self.__TimeStamps[0] > self.__timout:
            self.__TimeStamps.pop(0)
            self.__storedContours.pop(0)

    def isEmpty(self):
        return not self.__storedContours