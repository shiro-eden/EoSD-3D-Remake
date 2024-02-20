import numpy
import pygame

from math import pi

from GameParameteres import screen_height, screen_width
from MathOperations import rotate_x, rotate_y


class Camera:
    def __init__(self, position, speed):
        self.position = numpy.array([*position, 1.0])
        self.moving_speed = speed
        self.rotation_speed = 0.015

        self.angle_pitch = 0
        self.angle_yaw = 0
        self.angle_roll = 0

        self.forward = self.up = self.right = None
        self.make_default_direction()

        self.horizontal_angle_vision = pi / 3
        self.vertical_angle_vision = screen_height / screen_width * self.horizontal_angle_vision
        self.near_border_render = 0.01
        self.far_border_render = 100

    def render(self):
        # x, y = pygame.mouse.get_pos()
        # dx, dy = screen_half_width - x, screen_half_height - y

        # self.camera_rotate_yaw(dx)
        # self.camera_rotate_pitch(dy)

        # self.camera_update_matrix()

        # pygame.mouse.set_pos(screen_half_size)
        pass

    def camera_rotate_yaw(self, angle):
        self.angle_yaw += angle * self.moving_speed

    def camera_rotate_pitch(self, angle):
        self.angle_pitch += angle * self.moving_speed

    def make_default_direction(self):
        self.forward = numpy.array([0, 0, 1, 1])
        self.up = numpy.array([0, 1, 0, 1])
        self.right = numpy.array([1, 0, 0, 1])

    def get_rotate_camera(self):
        return rotate_x(self.angle_pitch) @ rotate_y(self.angle_yaw)

    def camera_update_matrix(self):
        rotate = self.get_rotate_camera()
        self.make_default_direction()
        self.forward = self.forward @ rotate
        self.right = self.right @ rotate
        self.up = self.up @ rotate

    def get_camera_matrix(self):
        self.camera_update_matrix()
        return self.move_to_SLU() @ self.rotate_matrix()

    def move_to_SLU(self):
        x, y, z, w = self.position
        return numpy.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [-x, -y, -z, 1]
        ])

    def move(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_a]:
            self.position -= self.right * self.moving_speed
        if key[pygame.K_d]:
            self.position += self.right * self.moving_speed
        if key[pygame.K_w]:
            self.position += self.forward * self.moving_speed
        if key[pygame.K_s]:
            self.position -= self.forward * self.moving_speed
        if key[pygame.K_q]:
            self.position += self.up * self.moving_speed
        if key[pygame.K_e]:
            self.position -= self.up * self.moving_speed

        if self.position[1] < 5:
            self.position[1] = 5

        if key[pygame.K_LEFT]:
            self.camera_rotate_yaw(-self.rotation_speed)
        if key[pygame.K_RIGHT]:
            self.camera_rotate_yaw(self.rotation_speed)
        if key[pygame.K_UP]:
            self.camera_rotate_pitch(-self.rotation_speed)
        if key[pygame.K_DOWN]:
            self.camera_rotate_pitch(self.rotation_speed)

    def rotate_matrix(self):
        rx, ry, rz, w = self.right
        fx, fy, fz, w = self.forward
        ux, uy, uz, w = self.up
        return numpy.array([
            [rx, ux, fx, 0],
            [ry, uy, fy, 0],
            [rz, uz, fz, 0],
            [0, 0, 0, 1]
        ])
