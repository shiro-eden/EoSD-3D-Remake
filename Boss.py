import numpy
import pygame

from Object import Object, any_func, Shadow
from GameParameteres import screen_half_size, screen


class Boss(Object):
    def __init__(self, position):
        super().__init__(None, 0.5)

        self.position = numpy.array([*position, 1], float)
        self.images = [pygame.image.load(f"flandre/flandre_stand_{i}.png") for i in range(8)]

        self.width, self.height = self.images[0].get_size()
        self.half_width, self.half_height = self.width // 2, self.height // 2
        self.vertices = numpy.array([numpy.array([*position, 1], float) for _ in range(4)])
        self.vertices[0] += numpy.array([self.width, self.height, 0, 0], float)
        self.vertices[1] += numpy.array([0, self.height, 0, 0], float)
        self.vertices[3] += numpy.array([self.width, 0, 0, 0], float)

        self.frame = 0
        self.count = 8
        self.scale = 1

        self.shadow = Shadow(position, 10)

    def update_frame(self, time):
        self.frame = int(time % self.count)

    def render(self, camera_matrix):

        vertices = self.screen_projection(camera_matrix)
        if not any_func(vertices, *screen_half_size):
            max_x, min_x = max([i[0] for i in vertices]), min([i[0] for i in vertices])
            max_y, min_y = max([i[1] for i in vertices]), min([i[1] for i in vertices])
            self.scale = abs(max_y - min_y) / self.height

            self.shadow.render(camera_matrix, min_x, min_x + self.width * self.scale)
            screen.blit(
                pygame.transform.scale(self.images[self.frame], (self.width * self.scale, self.height * self.scale)),
                (min_x, min_y))
