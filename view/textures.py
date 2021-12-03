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

        # Крестик и нолик
        self.figure = [pygame.image.load('png/cross.png'),
                       pygame.image.load('png/zero.png')]
