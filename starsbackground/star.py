class Star:
    """Класс, инкапсулирующий координаты, скорость, цвет и отображение на экране одной звезды."""

    screen_width = 0
    screen_height = 0

    def __init__(self, x, y, speed_x, speed_y, color):
        """Задаёт основные параметры звезды."""
        self.__x = x
        self.__y = y
        self.__speed_x = speed_x
        self.__speed_y = speed_y
        self.__color = color

    def moveX(self, delta):
        """Перемещает звезду влево, изменяя координату X."""
        self.__x += self.__speed_x * delta
        if self.__x < 0:
            self.__x = Star.screen_width

    def act(self, delta):
        """Изменение: одно за один кадр."""
        self.moveX(delta)

    def draw(self, pygame, scene):
        pygame.draw.circle(scene, self.__color, (self.__x, self.__y), 1, 1)