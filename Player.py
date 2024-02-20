import numpy as np
import pygame

from GameParameteres import screen_height, screen_half_width, screen


class Player:
    def __init__(self, position):
        self.position = np.array([*position, 1], float)
        self.images = {
            0: [pygame.image.load(f"remilia/stay/remilia_{i}.png") for i in range(8)],
            1: [pygame.image.load(f"remilia/left/remilia_{i}.png") for i in range(8)],
            2: [pygame.image.load(f"remilia/right/remilia_{i}.png") for i in range(8)]
        }
        self.width, self.height = self.images[0][0].get_size()
        self.movingSpeed = 0.5
        self.frame_moving = 0
        self.frame = 0
        self.count = 8

        self.condition = 0

    def update_frame(self, time):
        self.frame = time % self.count

    def render(self, time):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_d] or keys[pygame.K_a] or keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]:
            self.frame_moving = self.frame_moving if self.frame_moving == self.count - 1 else time % self.count
        elif self.frame_moving:
            self.frame_moving = self.count - time % self.count - 1
        else:
            self.update_frame(time)

        if self.frame_moving == 0:
            self.condition = 0
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.condition = 1
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.condition = 2

        if self.condition:
            screen.blit(self.images[self.condition][self.frame_moving],
                    (screen_half_width - self.width // 2, screen_height - self.height))
        else:
            screen.blit(self.images[self.condition][self.frame],
                    (screen_half_width - self.width // 2, screen_height - self.height))
