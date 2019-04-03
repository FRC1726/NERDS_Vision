#!/usr/bin/env python3

import math

def DistanceFromFrameBottom(fov, height):
    fov_radians = (fov * math.pi) / 180
    distance = height * math.tan(math.pi / 2 - (fov_radians / 2))
    return distance

def FloorDistance(y, screen, fov, height):
    fov_radians = fov * math.pi / 180
    c = (screen - y) / math.tan(fov_radians/2)
    b = DistanceFromFrameBottom(fov, height)
    return b + c