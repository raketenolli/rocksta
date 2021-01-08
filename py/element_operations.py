import numpy as np
from math import sqrt, pi, atan2, log

def normal(vector):
    normal_original_length = np.array([-1.0 * vector[1], vector[0]])
    return normalize(normal_original_length)

def tangent(vector):
    return normalize(vector)

def normalize(vector):
    length_squared = vector[0]**2.0 + vector[1]**2.0
    length = sqrt(length_squared)
    return vector / length

def convert_to_local_coordinates(point, point1, point2):
    local_x_axis = normalize(point2 - point1)
    local_y_axis = normal(local_x_axis)
    point_in_local_coordinates = np.array([np.dot(point - point1, local_x_axis), np.dot(point - point1, local_y_axis)])
    return point_in_local_coordinates

def convert_to_world_coordinates(point, point1, point2, *args):
    local_x_axis = normalize(point2 - point1)
    local_y_axis = normal(local_x_axis)
    if "dir" in args:
        point_in_world_coordinates = point[0] * local_x_axis + point[1] * local_y_axis
    else:
        point_in_world_coordinates = point1 + point[0] * local_x_axis + point[1] * local_y_axis
    return point_in_world_coordinates

def doublet_induced_velocity_local(point, point1, point2):
    x = point[0]
    y = point[1]
    x1 = point1[0]
    y1 = point1[1]
    x2 = point2[0]
    y2 = point2[1]
    u = 1.0 / (2.0 * pi) * (y / ((x - x1)**2.0 + y**2.0) - y / ((x - x2)**2.0 + y**2.0))
    w = -1.0 / (2.0 * pi) * ((x - x1) / ((x - x1)**2.0 + y**2.0) - (x - x2) / ((x - x2)**2.0 + y**2.0))
    return np.array([u, w])

def vortex_induced_velocity_local(point, point1, point2):
    x = point[0]
    y = point[1]
    x1 = point1[0]
    y1 = point1[1]
    x2 = point2[0]
    y2 = point2[1]
    u = 1.0 / (2.0 * pi) * (atan2(y - y2, x - x2) - atan2(y - y1, x - x1))
    w = - 1.0 / (4.0 * pi) * log(((x - x1)**2 + (y - y1)**2) / ((x - x2)**2 + (y - y2)**2))
    return np.array([u, w])

def doublet_induced_velocity_world(point, point1, point2):
    point_local = convert_to_local_coordinates(point, point1, point2)
    point1_local = convert_to_local_coordinates(point1, point1, point2)
    point2_local = convert_to_local_coordinates(point2, point1, point2)
    induced_velocity_in_local_coordinates = doublet_induced_velocity_local(point_local, point1_local, point2_local)
    induced_velocity_in_world_coordinates = convert_to_world_coordinates(induced_velocity_in_local_coordinates, point1, point2, "dir")
    return induced_velocity_in_world_coordinates

def vortex_induced_velocity_world(point, point1, point2):
    point_local = convert_to_local_coordinates(point, point1, point2)
    point1_local = convert_to_local_coordinates(point1, point1, point2)
    point2_local = convert_to_local_coordinates(point2, point1, point2)
    induced_velocity_in_local_coordinates = vortex_induced_velocity_local(point_local, point1_local, point2_local)
    induced_velocity_in_world_coordinates = convert_to_world_coordinates(induced_velocity_in_local_coordinates, point1, point2, "dir")
    return induced_velocity_in_world_coordinates