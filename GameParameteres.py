from pygame import display
from math import tan, pi
import numpy


screen_size = screen_width, screen_height = 1280, 720
screen_half_size = screen_half_width, screen_half_height = 640, 360

FPS = 60

NEAR = 0.1
FAR = 100
projection_matrix = numpy.array([
            [1 / tan(pi / 6), 0, 0, 0],
            [0, 1 / tan(screen_height / screen_width * pi / 12), 0, 0],
            [0, 0, (FAR + NEAR) / (FAR - NEAR), 1],
            [0, 0, -2 * NEAR * FAR / (FAR - NEAR), 0]
        ])

to_screen_matrix = numpy.array([
            [screen_half_width, 0, 0, 0],
            [0, -screen_half_height, 0, 0],
            [0, 0, 1, 0],
            [screen_half_width, screen_half_height, 0, 1]
        ])

screen = display.set_mode(screen_size)