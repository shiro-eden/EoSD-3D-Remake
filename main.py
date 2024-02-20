import pygame

from GameParameteres import screen_size, FPS, screen
from Game import GameWindow


class ScreenHolder:
    def __init__(self):
        pygame.init()
        pygame.mouse.set_visible(False)
        pygame.mouse.set_pos(screen_size)
        self.clock = pygame.time.Clock()
        self.start_time = pygame.time.get_ticks()

        self.game = True

        self.ActiveWindow = GameWindow()

    def start(self):
        while self.game:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game = False

            time = (pygame.time.get_ticks() - self.start_time) * 8 // 1000
            self.ActiveWindow.render(time)

            pygame.display.set_caption(str(int(self.clock.get_fps())))
            pygame.display.flip()
            screen.fill((0, 150, 100))
            self.clock.tick(FPS)


if __name__ == '__main__':
    MainWindow = ScreenHolder()
    MainWindow.start()
