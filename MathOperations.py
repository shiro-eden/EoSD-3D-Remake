from math import cos, sin
import numpy


def move_to_position(position):
    x, y, z = position
    return numpy.array([
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [x, y, z, 1]
    ], float)


def rotate_x(a):
    return numpy.array([
        [1, 0, 0, 0],
        [0, cos(a), sin(a), 0],
        [0, -sin(a), cos(a), 0],
        [0, 0, 0, 1]
    ])


def rotate_y(a):
    return numpy.array([
        [cos(a), 0, -sin(a), 0],
        [0, 1, 0, 0],
        [sin(a), 0, cos(a), 0],
        [0, 0, 0, 1]
    ])


def rotate_z(a):
    return numpy.array([
        [cos(a), sin(a), 0, 0],
        [-sin(a), cos(a), 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ])


def scale(n):
    return numpy.array([
        [n, 0, 0, 0],
        [0, n, 0, 0],
        [0, 0, n, 0],
        [0, 0, 0, 1]
    ])