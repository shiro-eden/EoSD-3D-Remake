import numpy
import pygame

from numba import njit

from GameParameteres import projection_matrix, to_screen_matrix, screen, screen_half_size
from MathOperations import rotate_x, rotate_y, rotate_z, scale, move_to_position


@njit(fastmath=True)
def any_func(arr, a, b):
    return numpy.any((arr == a) | (arr == b))


class Object:
    def __init__(self, vertices, speed):
        self.vertices = vertices  # вершины
        self.movingSpeed = speed

    def screen_projection(self, camera_matrix):
        vertices = self.vertices @ camera_matrix  # перенос в ЛСУ камеры
        vertices = vertices @ projection_matrix  # проектирование
        vertices /= vertices[:, -1].reshape(-1, 1)  # нормализация
        vertices[(vertices > 2) | (vertices < -2)] = 0  # убрать не отображающиеся точки
        vertices = vertices @ to_screen_matrix  # проектирование на экран
        vertices = vertices[:, :2]
        return vertices

    def move(self, direction):
        self.vertices = self.vertices @ move_to_position(direction * self.movingSpeed)

    def scale(self, scale_to):
        self.vertices = self.vertices @ scale(scale_to)

    def rotate_x(self, angle):
        self.vertices = self.vertices @ rotate_x(angle)

    def rotate_y(self, angle):
        self.vertices = self.vertices @ rotate_y(angle)

    def rotate_z(self, angle):
        self.vertices = self.vertices @ rotate_z(angle)


class SpriteObject(Object):
    def __init__(self, vertices, speed, name, count):
        super().__init__(vertices, speed)
        self.image = [pygame.image.load(f"{name}/{name}_stand_{i}.png") for i in range(count)]
        self.frame = 0
        self.scale = 1
        self.width, self.height = 1, 1
        self.count = count

    def render(self, camera_matrix):
        vertices = self.screen_projection(camera_matrix)
        self.scale = (vertices[3][0] - vertices[0][0]) / self.width
        screen.blit(pygame.transform.scale(self.image[self.frame], (self.width * self.scale, self.height * self.scale)))


class Plane(Object):
    def __init__(self):
        vertices = numpy.array([(-20, 0, -20, 1), (-20, 0, 20, 1), (20, 0, 20, 1), (20, 0, -20, 1)])
        super().__init__(vertices, 0)

    def render(self, camera_matrix):
        vertices = self.screen_projection(camera_matrix)
        if not any_func(vertices, *screen_half_size):
            pygame.draw.polygon(screen, "crimson", vertices)


class Shadow(Object):
    def __init__(self, position, radius):
        super().__init__(None, 0)

        self.radius = radius
        self.vertices = numpy.array([numpy.array([*position, 1], float) for _ in range(4)])
        for i in range(4):
            self.vertices[i][1] = 0
        self.vertices[0] += numpy.array([-radius, 0, -radius, 0], float)
        self.vertices[1] += numpy.array([-radius, 0, radius, 0], float)
        self.vertices[2] += numpy.array([radius, 0, radius, 0], float)
        self.vertices[3] += numpy.array([radius, 0, -radius, 0], float)

    def render(self, camera_matrix, min_cords_x, max_cords_x):
        vertices = self.screen_projection(camera_matrix)
        if not any_func(vertices, *screen_half_size):
            max_y, min_y = max([i[1] for i in vertices]), min([i[1] for i in vertices])
            pygame.draw.ellipse(screen, "black", (min_cords_x, min_y, max_cords_x - min_cords_x, max_y - min_y))


class Axes(Object):
    def __init__(self):
        vertices = numpy.array([(0, 0, 0, 1), (10, 0, 0, 1), (0, 10, 0, 1), (0, 0, 10, 1)])
        self.faces = numpy.array([(0, 1), (0, 2), (0, 3)])
        super().__init__(vertices, 0.1)

    def render(self, camera_matrix):
        vertices = self.screen_projection(camera_matrix)
        c = 0
        color = ["red", "blue", "green"]
        for face in self.faces:
            polygon = vertices[face]
            if not any_func(polygon, *screen_half_size):
                pygame.draw.polygon(screen, color[c], polygon, 5)
                c += 1


class Parallelepiped(Object):
    def __init__(self, position):
        super().__init__(None, 0.1)

        self.position = position
        self.vertices = numpy.array([numpy.array([*position, 1], float) for _ in range(6)])

        length_x = 5
        length_y = 2
        length_z = 3

        self.vertices[0] += [length_x, 0, 0, 0]
        self.vertices[1] += [0, length_y, 0, 0]
        self.vertices[2] += [-length_x, 0, 0, 0]
        self.vertices[3] += [0, -length_y, 0, 0]
        self.vertices[4] += [0, 0, length_z, 0]
        self.vertices[5] += [0, 0, -length_z, 0]

        self.faces = numpy.array([(0, 1, 4), (0, 3, 4), (0, 1, 5), (0, 3, 5),
                                  (2, 1, 4), (2, 3, 4), (2, 1, 5), (2, 3, 5)])

    def render(self, camera_matrix):
        vertices = self.screen_projection(camera_matrix)

        for face in self.faces:
            polygon = vertices[face]
            if not any_func(polygon, *screen_half_size):
                pygame.draw.polygon(screen, "lightblue", polygon)

        for vertex in vertices:
            if not any_func(vertex, *screen_half_size):
                pygame.draw.circle(screen, pygame.Color('white'), vertex, 2)