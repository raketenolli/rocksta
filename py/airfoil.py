import numpy as np
from math import pi, cos, sqrt
from matplotlib import pyplot as plt
from element_operations import *

class NACA00xx:
    def __init__(self, thickness, number_of_elements):
        self._points = np.zeros((number_of_elements + 1, 2))
        half_number_of_elements = number_of_elements / 2
        for i in range(number_of_elements + 1):
            theta = pi * i / number_of_elements
            x = cos(theta)**2.0
            self._points[i, 0] = x
            y = (-1 if i < half_number_of_elements else 1) * 5 * thickness * (0.2969 * sqrt(x) - 0.1260 * x - 0.3516 * x**2.0 + 0.2843 * x**3.0 - 0.1015 * x**4.0)
            self._points[i, 1] = y
        self._elements = np.zeros((number_of_elements, 2), dtype=np.int)
        for i in range(number_of_elements):
            self._elements[i, 0] = i
            self._elements[i, 1] = i + 1
        self._wake_element = np.array([[1.0, 0.0], [10000.0, 0.0]])

    def points(self):
        return self._points

    def element_indices(self):
        return self._elements

    def element_points(self):
        return self._points[self._elements]
    
    def element_midpoints(self):
        return (self.element_points()[:, 0, :] + self.element_points()[:, 1, :]) / 2.0
    
    def element_normals(self):
        return np.array([normal(element_ends[1] - element_ends[0]) for element_ends in self.element_points()])

    def wake_element(self):
        return self._wake_element

    def plot(self, *args):
        fig = plt.figure()
        ax = fig.add_subplot()
        ax.set_aspect('equal')
        if "p" in args or "points" in args:
            ax.scatter(self._points[:, 0], self._points[:, 1])
        if "e" in args or "elements" in args:
            points = self.element_points().reshape((-1, 2))
            ax.plot(points[:, 0], points[:, 1])
        return (fig, ax)
