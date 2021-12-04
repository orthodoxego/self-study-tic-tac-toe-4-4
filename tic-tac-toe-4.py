import pygame
from setup import Setup
from model.engine import TicTacEngine

class Game:
    """Класс-шаблон для игр на базе pygame."""

    def __init__(self, width, height, caption):
        """Конструктор, настройка основных параметров."""
        pygame.init()

        self.setup = Setup()

        if width + height == 0:
            width = pygame.display.Info().current_w
            height = pygame.display.Info().current_h
            self.scene = pygame.display.set_mode(flags=pygame.FULLSCREEN)
        else:
            self.__size = [width, height]
            self.scene = pygame.display.set_mode(self.__size)
            pygame.display.set_caption(caption)

        self.setup.screen_width = width
        self.setup.screen_height = height

        self.__size = [self.setup.screen_width, self.setup.screen_height]
        self.clock = pygame.time.Clock()

        self.playGame = True
        self.__delta = 0

        # Игровой движок (модель)
        # Она же создаёт и представление, и контроллер, и игровые объекты
        self.__tic_tac_toe = TicTacEngine()

    @property
    def WIDTH(self):
        return self.setup.screen_width

    @property
    def HEIGHT(self):
        return self.setup.screen_height

    def run(self):
        """Главный цикл игры."""
        while (self.playGame):

            # Отрисовка
            self.scene.fill(self.setup.BLACK)
            self.__tic_tac_toe.draw(self.scene, self.clock)
            pygame.display.flip()

            # Клавиатура + расчёты
            self.playGame = self.__tic_tac_toe.controller(pygame, self.__delta)
            self.playGame *= self.__tic_tac_toe.act(pygame, self.__delta)

            # Delta-time для коррекции анимации
            self.__delta = self.clock.tick(self.setup.FPS) / 1000

        pygame.quit()


if __name__ == "__main__":
    game = Game(Setup().screen_width, Setup().screen_height, "TIC-TAC-TOE 4x4")
    # game = Game(0, 0, "TIC-TAC-TOE 4x4")
    game.run()
