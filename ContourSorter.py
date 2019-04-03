 #!/usr/bin/env python3

import cv2
import numpy as np
import SimilarContours

class ContourSorter:
    
    def __init__(self, tolerance, maxContour, TimeOuts):
        self.__ContourCollection = []
        self.__Tolerance = tolerance
        self.__MaxContours = maxContour
        self.__TimeOuts = TimeOuts

    def CompareContours(self, Contour):
        for SimilarCollection in self.__ContourCollection:
            SimilarCollection.removeOld()
            if SimilarContours.isEmpty()
                __ContourCollection.remove(SimilarCollection)


        if not self.__ContourCollection:
            self.__ContourCollection.append(SimilarContours.SimilarContours(self.__MaxContours,self.__Timeouts))
            self.__ContourCollection[-1].insertContours(Contour)
            return
        
        index = 0
        for SimilarCollection in self.__ContourCollection:
            AvgDifference = SimilarCollection.checkContours(Contour)
            if lowest > AvgDifference:
                lowest = AvgDifference
                lowestIndex = index

            index++
        
        if lowest < self.__Tolerance:
            self.__ContourCollection[lowestIndex].insertContours(Contour)
        else:
            self.__ContourCollection.append(SimilarContours.SimilarContours(self.__MaxContours,self.__Timeouts))
            self.__ContourCollection[-1].insertContours(Contour)
            