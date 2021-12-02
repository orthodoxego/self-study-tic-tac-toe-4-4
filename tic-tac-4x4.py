import pygame
from setup import Setup
from model.tictacengine import TicTacEngine

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
        self.__tic_tac_toe = TicTacEngine()

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

            self.playGame = self.__tic_tac_toe.act(pygame, self.__delta / 1000)
            self.__tic_tac_toe.draw(self.scene, self.__delta)

            pygame.display.flip()
            self.__delta = self.clock.tick(Setup.FPS)
        pygame.quit()


if __name__ == "__main__":
    game = Game(Setup.screen_width, Setup.screen_height, "TIC-TAC-TOE 4x4")
    # game = Game(0, 0, "TIC-TAC-TOE 4x4")
    game.run()
