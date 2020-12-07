import numpy as np
from math import pi, cos, sqrt
from matplotlib import pyplot as plt

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

    def elements(self):
        pass

    def plot(self):
        plt.figure()
        plt.axes().set_aspect('equal')
        plt.scatter(self._points[:, 0], self._points[:, 1])
        plt.show()