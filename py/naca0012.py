import numpy as np
import airfoil
from element_operations import *

number_of_elements = 20
naca0012 = airfoil.NACA00xx(0.12, number_of_elements)

points = naca0012.element_points()
midpoints = naca0012.element_midpoints()
normals = naca0012.element_normals()

naca0012.plot("p", "e")

influence_matrix = np.zeros((number_of_elements + 1, number_of_elements + 1))
for i in range(number_of_elements):
    for j in range(number_of_elements):
        # influence of element j onto element i
        v = induced_velocity_world(midpoints[i], points[j, 0], points[j, 1])
        n = normals[i]
        influence_matrix[i, j] = np.dot(v, n)

