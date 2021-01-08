import numpy as np
import airfoil
from element_operations import *
from math import sin, cos, pi
import matplotlib.pyplot as plt

number_of_elements = 100
naca0012 = airfoil.NACA00xx(0.12, number_of_elements)

points = naca0012.element_points()
midpoints = naca0012.element_midpoints()
normals = naca0012.element_normals()
tangents = naca0012.element_tangents()
wake = naca0012.wake_element()

print("points:", points)
print("midpoints:", midpoints)

angle_of_attack = 5 # degree
relative_wind_vector = np.array([cos(angle_of_attack * pi / 180.0), sin(angle_of_attack * pi / 180.0)])
print('relative wind:', relative_wind_vector)

### CONSTANT DOUBLET

# influence_matrix = np.zeros((number_of_elements + 1, number_of_elements + 1))
# for i in range(number_of_elements):
#     for j in range(number_of_elements):
#         # influence of element j onto element i
#         v = doublet_induced_velocity_world(midpoints[i], points[j, 0], points[j, 1])
#         n = normals[i]
#         influence_matrix[i, j] = np.dot(v, n)
# for i in range(number_of_elements):
#     # influence of wake element onto element i
#     v = doublet_induced_velocity_world(midpoints[i], wake[0], wake[1])
#     n = normals[i]
#     influence_matrix[i, number_of_elements] = np.dot(v, n)

# influence_matrix[number_of_elements, 0] = 1.0
# influence_matrix[number_of_elements, number_of_elements - 1] = -1.0
# influence_matrix[number_of_elements, number_of_elements] = 1.0

# print(influence_matrix)

# right_hand_side_vector = np.zeros((number_of_elements + 1))
# for i in range(number_of_elements):
#     right_hand_side_vector[i] = -1.0 * np.dot(relative_wind_vector, normals[i])
# print(right_hand_side_vector)

# doublet_strengths = np.linalg.solve(influence_matrix, right_hand_side_vector)
# print(doublet_strengths)

###

### CONSTANT VORTEX

influence_matrix = np.zeros((number_of_elements, number_of_elements))
for i in range(number_of_elements - 1):
    for j in range(number_of_elements):
        # influence of element j onto element i
        if i != j:
            v = vortex_induced_velocity_world(midpoints[i], points[j, 0], points[j, 1])
            t = tangents[i]
            influence_matrix[i, j] = np.dot(v, t)
        else:
            influence_matrix[i, j] = -1.0 / 2.0

influence_matrix[number_of_elements - 1, 0] = 1.0
influence_matrix[number_of_elements -1, number_of_elements - 1] = 1.0

print("Influence matrix:", influence_matrix)

right_hand_side_vector = np.zeros((number_of_elements))
for i in range(number_of_elements - 1):
    right_hand_side_vector[i] = -1.0 * np.dot(relative_wind_vector, tangents[i])
print("Right hand side vector:", right_hand_side_vector)

vortex_strengths = np.linalg.solve(influence_matrix, right_hand_side_vector)
print("Vortex strengths:", vortex_strengths)

###

(fig, ax) = naca0012.plot("p", "e")
ax.arrow(0, 0, 0.1 * relative_wind_vector[0], 0.1 * relative_wind_vector[1], length_includes_head=True, color="green", width=0.003)
for i in range(number_of_elements):
    # FOR DOUBLETS
    # ax.arrow(midpoints[i, 0], midpoints[i, 1], 0.1 * doublet_strengths[i] * normals[i, 0], 0.1 * doublet_strengths[i] * normals[i, 1], length_includes_head=True)
    # ax.arrow(midpoints[i, 0], midpoints[i, 1], 0.1 * right_hand_side_vector[i] * normals[i, 0], 0.1 * right_hand_side_vector[i] * normals[i, 1], length_includes_head=True)
    # ax.arrow(midpoints[i, 0] + 0.1 * right_hand_side_vector[i] * normals[i, 0], midpoints[i, 1] + 0.1 * right_hand_side_vector[i] * normals[i, 1], 0.1 * relative_wind_vector[0], 0.1 * relative_wind_vector[1], color="green", length_includes_head=True)

    # FOR VORTICES
    ax.arrow(midpoints[i, 0], midpoints[i, 1], 0.1 * vortex_strengths[i] * normals[i, 0], 0.1 * vortex_strengths[i] * normals[i, 1], length_includes_head=True, color="blue")
    ax.arrow(midpoints[i, 0], midpoints[i, 1], 0.1 * right_hand_side_vector[i] * tangents[i, 0], 0.1 * right_hand_side_vector[i] * tangents[i, 1], length_includes_head=True)


### CONSTANT DOUBLET

# local_velocities = np.zeros((number_of_elements, 2))
# print_values = False
# for i in range(number_of_elements):
#     if i == number_of_elements - 1:
#         print_values = True
#     local_velocities[i, :] = relative_wind_vector
#     if print_values: print(local_velocities[i, :])
#     for j in range(number_of_elements):
#         # influence of element j onto element i
#         v = doublet_strengths[j] * doublet_induced_velocity_world(midpoints[i], points[j, 0], points[j, 1])
#         local_velocities[i, :] += v
#         if print_values: print("element", j, "influence:", v, local_velocities[i, :])
#     # # influence of wake element onto element i
#     v = doublet_strengths[number_of_elements] * doublet_induced_velocity_world(midpoints[i], wake[0], wake[1])
#     local_velocities[i, :] += v
#     if print_values: print("wake influence:", v, local_velocities[i, :])
# print(local_velocities)

###


### CONSTANT VORTEX

local_velocities = np.zeros((number_of_elements, 2))
print_values = False
for i in range(number_of_elements):
    if i == 61:
        print_values = True
    local_velocities[i, :] = relative_wind_vector
    if print_values: print(local_velocities[i, :])
    for j in range(number_of_elements):
        # influence of element j onto element i
        if i != j:
            v = vortex_strengths[j] * vortex_induced_velocity_world(midpoints[i], points[j, 0], points[j, 1])
        else:
            v = vortex_strengths[j] * convert_to_world_coordinates(np.array([0.5, 0]), naca0012.element_points()[i, 0, :], naca0012.element_points()[i, 1, :], "dir")
        local_velocities[i, :] += v
        if print_values: print("element", j, "influence:", v, local_velocities[i, :])
    print_values = False
print(local_velocities)

###


# for i in range(number_of_elements):
#     ax.arrow(midpoints[i, 0], midpoints[i, 1], 0.1 * local_velocities[i, 0], 0.1 * local_velocities[i, 1], color="red", length_includes_head=True)

fig.show()

coefficients_of_pressure = np.zeros(number_of_elements)
for i in range(number_of_elements):
    coefficients_of_pressure[i] = 1.0 - (local_velocities[i, 0]**2.0 + local_velocities[i, 1]**2.0)

cpfig = plt.figure()
cpax = cpfig.add_subplot()
print("element points shape:", naca0012.element_points().shape)
print("coefficients of pressure shape:", coefficients_of_pressure.shape)
cpax.scatter(naca0012.element_points()[:, 0, 0], coefficients_of_pressure)
cpax.invert_yaxis()
cpfig.show()

input()
