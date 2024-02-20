import numpy

from random import randrange

from Player import Player
from Camera import Camera
from Boss import Boss
from Object import Axes, Plane, Parallelepiped


class GameWindow:
    def __init__(self):
        self.player = Player(numpy.array([20, 10, -120], float))
        self.camera = Camera(numpy.array([20, 10, -120], float), self.player.movingSpeed)
        self.camera.camera_rotate_pitch(-self.camera.rotation_speed * 3)
        self.camera.camera_rotate_yaw(-self.camera.rotation_speed * 3)
        self.boss = Boss(numpy.array([20, 0, 0], float))

        self.rombs = [Parallelepiped((
            randrange(-100, 100),
            randrange(-100, 100),
            randrange(-100, 100)
        )) for _ in range(10)]

        self.plane = Plane()
        self.axes = Axes()

    def render(self, time):
        camera_matrix = self.camera.get_camera_matrix()

        if self.plane:
            self.plane.render(camera_matrix)

        self.axes.render(camera_matrix)

        if self.rombs:
            for romb in self.rombs:
                romb.render(camera_matrix)

            self.rombs[randrange(0, 5)].move(numpy.array([randrange(-10, 10), randrange(-10, 10), randrange(-10, 10)]))

        if self.camera:
            self.camera.move()
            self.camera.render()

        if self.boss:
            self.boss.render(camera_matrix)
            self.boss.update_frame(time)

        if self.player:
            self.player.position = self.camera.position
            self.player.render(time)
