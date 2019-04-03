#!/usr/bin/env python3

import cv2
import numpy as np
import math

class Projection:

    def __init__(self, d_pov, resolution):
        ratio = resolution[1] / resolution[0]

        self._v_pov = math.radians(d_pov / math.sqrt(1 + (ratio) ** 2))
        self._h_pov = math.radians(d_pov / math.sqrt(1 + (ratio) ** 2) * ratio)

        self._h_resolution = resolution[0]
        self._v_resolution = resolution[1]

        self._pitch = 0
        self._yaw = 0

    def draw(self, image):
        pass

    def set_angle(self, pitch, yaw):
        self._pitch = math.radians(pitch)
        self._yaw = math.radians(yaw)

    def _find_screen_size(self, distance):
        width = 2 * distance * math.tan(self._h_pov / 2)
        height = 2 * distance * math.tan(self._v_pov / 2)

        return width, height

    def _find_point(self, x_point, y_point, z_point):
        if self._pitch != 0:
            z_point, y_point = self._transform_point(z_point, y_point, self._pitch)

        if self._yaw != 0:
            x_point, y_point = self._transform_point(x_point, y_point, self._yaw)

        width, height = self._find_screen_size(y_point)

        x_point = (self._h_resolution / 2) + (self._h_resolution * (x_point / width))
        y_point = (self._v_resolution / 2) - (self._v_resolution * (z_point / height))

        return (int(x_point), int(y_point))

    def _transform_point(self, x_point, y_point, angle):
        a_prime = x_point / math.cos(angle)
        b_prime = x_point * math.tan(angle)

        b = y_point - b_prime
        a = b * math.sin(angle)

        new_x = a + a_prime
        new_y = b * math.cos(angle)

        return new_x, new_y

class RobotGuide(Projection):

    def __init__(self, d_pov, resolution, robot_width):
        Projection.__init__(self, d_pov, resolution)
        
        self._robot_width = robot_width

        self._markers = []

        self._x_offset = 0
        self._y_offset = 0
        self._z_offset = 0
        
    def add_marker(self, distance, color):
        marker = (distance, color)
        self._markers.append(marker)
        self._markers.sort(key=lambda tup: tup[0])

    def set_offset(self, x, y, z):
        self._x_offset = x
        self._y_offset = y
        self._z_offset = z

    def draw(self, image):
        floor_distance = math.tan((self._v_pov / 2) - self._pitch) * self._z_offset + self._y_offset
        
        x_left = -self._robot_width / 2 - self._x_offset
        x_right = self._robot_width / 2 - self._x_offset

        left_previous = self._find_point(x_left, floor_distance, -self._z_offset)
        right_previous = self._find_point(x_right, floor_distance, -self._z_offset)

        for distance, color in self._markers:
            if distance > floor_distance:
                left = self._find_point(x_left, distance, -self._z_offset)
                right = self._find_point(x_right, distance, -self._z_offset)

                cv2.line(image, left_previous, left, color, 2)
                cv2.line(image, right_previous, right, color, 2)
                cv2.line(image, left, right, color, 2)

                left_previous = left
                right_previous = right


class Reticle(Projection):

    def __init__(self, d_pov, resolution):
        Projection.__init__(self, d_pov, resolution)

        self._markers = []

        self._x_offset = 0
        self._y_offset = 0
        self._z_offset = 0
        
    def add_marker(self, position, radius, color):
        marker = (position, radius, color)
        self._markers.append(marker)
        self._markers.sort(key=lambda tup: tup[0])

    def set_offset(self, x, y, z):
        self._x_offset = x
        self._y_offset = y
        self._z_offset = z

    def draw(self, image):
        for position, radius, color in self._markers:
            x = position[0] - self._x_offset
            y = position[1] - self._y_offset
            z = position[2] - self._z_offset

            screen_size = self._find_screen_size(y)

            target_radius = int(radius / screen_size[0] * self._h_resolution)

            center = self._find_point(x, y, z)

            cv2.circle(image, center, target_radius, color, 2)