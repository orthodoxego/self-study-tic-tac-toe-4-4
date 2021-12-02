import pygame
from setup import Setup

class Game:
    """Класс-шаблон для игр на базе pygame."""

    def __init__(self, width, height, caption):
        """Конструктор, настройка основных параметров."""
        pygame.init()

        if width + height == 0:
            width = pygame.display.Info().current_w
            height = pygame.display.Info().current_h
            self.scene = pygame.display.set_mode(flags=pygame.FULLSCREEN)
        else:
            self.__size = [width, height]
            self.scene = pygame.display.set_mode(self.__size)
            pygame.display.set_caption(caption)

        Setup.screen_width = width
        Setup.screen_height = height

        self.__size = [Setup.screen_width, Setup.screen_height]
        self.clock = pygame.time.Clock()

        self.playGame = True
        self.__delta = 0

        # Игровой движок (модель)
        # Она же создаёт и представление, и контроллер, и игровые объекты

    @property
    def WIDTH(self):
        return self.__WIDTH

    @property
    def HEIGHT(self):
        return self.__HEIGHT

    def run(self):
        """Главный цикл игры."""
        while (self.playGame):
            self.scene.fill(Setup.BLACK)
            # self.__hit_engine.draw(self.scene)
            # self.playGame = self.__hit_engine.act(pygame, self.__delta / 1000)
            pygame.display.flip()
            self.__delta = self.clock.tick(Setup.FPS)
        pygame.quit()


if __name__ == "__main__":
    game = Game(Setup.screen_width, Setup.screen_height, "TIC-TAC-TOE 4x4")
    # game = Game(0, 0, "TIC-TAC-TOE 4x4")
    game.run()
