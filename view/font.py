import pygame

class Font:
    """Генерирует поверхности с текстом для вывода на экран."""
    def __init__(self):
        """Определяет шрифты."""
        self.__font_system = pygame.font.Font("font\\roboto-regular.ttf", 16)
        self.__font_big = pygame.font.Font("font\\roboto-regular.ttf", 30)
        self.__texts = {}
        self.__surfaces = {}

    def getSystemText(self, key, text, color):
        """Вернёт поверхность с текстом."""
        if key in self.__texts:
            if text == self.__texts[key]:
                return self.__surfaces[key]
        self.__texts[key] = text
        self.__surfaces[key] = self.__font_system.render(text, True, color)
        return self.__surfaces[key]

    def getBigText(self, key, text, color):
        """Вернёт поверхность с текстом."""
        if key in self.__texts:
            if text == self.__texts[key]:
                return self.__surfaces[key]
        self.__texts[key] = text
        self.__surfaces[key] = self.__font_big.render(text, True, color)
        return self.__surfaces[key]