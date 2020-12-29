import numpy as np
import airfoil
from element_operations import *
from math import sin, cos, pi

number_of_elements = 20
naca0012 = airfoil.NACA00xx(0.12, number_of_elements)

points = naca0012.element_points()
midpoints = naca0012.element_midpoints()
normals = naca0012.element_normals()
wake = naca0012.wake_element()

angle_of_attack = 1 # degree
relative_wind_vector = np.array([cos(angle_of_attack * pi / 180.0), sin(angle_of_attack * pi / 180.0)])
print('relative wind:', relative_wind_vector)

influence_matrix = np.zeros((number_of_elements + 1, number_of_elements + 1))
for i in range(number_of_elements):
    for j in range(number_of_elements):
        # influence of element j onto element i
        v = induced_velocity_world(midpoints[i], points[j, 0], points[j, 1])
        n = normals[i]
        influence_matrix[i, j] = np.dot(v, n)
for i in range(number_of_elements):
    # influence of wake element onto element i
    v = induced_velocity_world(midpoints[i], wake[0], wake[1])
    n = normals[i]
    influence_matrix[i, number_of_elements] = np.dot(v, n)

influence_matrix[number_of_elements, 0] = 1.0
influence_matrix[number_of_elements, number_of_elements - 1] = -1.0
influence_matrix[number_of_elements, number_of_elements] = 1.0

print(influence_matrix)

right_hand_side_vector = np.zeros((number_of_elements + 1))
for i in range(number_of_elements):
    right_hand_side_vector[i] = -1.0 * np.dot(relative_wind_vector, normals[i])
print(right_hand_side_vector)

doublet_strengths = np.linalg.solve(influence_matrix, right_hand_side_vector)
print(doublet_strengths)

(fig, ax) = naca0012.plot("p", "e")
for i in range(number_of_elements):
    ax.arrow(midpoints[i, 0], midpoints[i, 1], 0.1 * right_hand_side_vector[i] * normals[i, 0], 0.1 * right_hand_side_vector[i] * normals[i, 1], length_includes_head=True)
    ax.arrow(midpoints[i, 0] + 0.1 * right_hand_side_vector[i] * normals[i, 0], midpoints[i, 1] + 0.1 * right_hand_side_vector[i] * normals[i, 1], 0.1 * relative_wind_vector[0], 0.1 * relative_wind_vector[1], color="green", length_includes_head=True)

local_velocities = np.zeros((number_of_elements, 2))
for i in range(number_of_elements):
    local_velocities[i, :] = relative_wind_vector
    for j in range(number_of_elements):
        # influence of element j onto element i
        v = doublet_strengths[j] * induced_velocity_world(midpoints[i], points[j, 0], points[j, 1])
        local_velocities[i, :] += v
    # influence of wake element onto element i
    v = doublet_strengths[number_of_elements] * induced_velocity_world(midpoints[i], wake[0], wake[1])
    local_velocities[i, :] += v
print(local_velocities)

for i in range(number_of_elements):
    ax.arrow(midpoints[i, 0], midpoints[i, 1], 0.1 * local_velocities[i, 0], 0.1 * local_velocities[i, 1], color="red", length_includes_head=True)

fig.show()
input()
