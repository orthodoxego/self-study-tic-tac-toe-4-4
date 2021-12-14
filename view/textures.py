import pygame
from setup import Setup

class Textures:
    """Загружает из файлов и хранит изображения."""

    def __init__(self):

        self.setup = Setup()

        # Клетка
        self.cell = pygame.image.load('png/cell.png')

        # Выделенная клетка
        self.cell_select = pygame.image.load('png/cell_select.png')

        # Запрещённая для установки клетка
        self.cell_district = pygame.image.load('png/cell_district.png')

        # Клетка-подсветка победившей комбинации
        self.cell_win = pygame.image.load('png/cell_win.png')

        # Крестик и нолик
        self.__figure = [
            [pygame.image.load('png/cross.png'), pygame.image.load('png/zero.png')],
            [pygame.image.load('png/cross-diamond.png'), pygame.image.load('png/zero-diamond.png')],
            [pygame.image.load('png/apple8bit.png'), pygame.image.load('png/pear8bit.png')],
            [pygame.image.load('png/smile01.png'), pygame.image.load('png/smile02.png')],
            [pygame.image.load('png/tile01.png'), pygame.image.load('png/tile02.png')]
             ]

    @property
    def figure(self):
        return self.__figure[self.setup.skin_number]
