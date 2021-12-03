class Single(type):
    """Шаблон Singleton без инициализации."""
    _instance = None
    def __call__(self, *args, **kwargs):
        if not Single._instance:
            Single._instance = super(Single, self).__call__(*args, **kwargs)
        return Single._instance

class Setup(metaclass=Single):
    """Настройки игры."""
    def __init__(self):
        # ФПС
        self.FPS = 60  # Минимальное 10

        # Ширина и высота окна для оконного режима
        self._screen_width = 1024
        self._screen_height = 768

        # Номера фигур
        self.figure01 = 0
        self.figure02 = 1
        self.clear_field = 10

        # Размер доски X * X
        self.board_lenght = 5
        self.setStartPoint()

        # Цвета
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)
        self.BLUE = (0, 0, 255)

    @property
    def screen_width(self):
        return self._screen_width

    @screen_width.setter
    def screen_width(self, value):
        self._screen_width = value
        self.setStartPoint()

    @property
    def screen_height(self):
        return self._screen_height

    @screen_height.setter
    def screen_height(self, value):
        self._screen_height = value
        self.setStartPoint()

    def setStartPoint(self):
        self.start_point_x, self.start_point_y = self.getStartPoint()

    def getStartPoint(self):
        """Вернёт координату левого верхнего угла игрового поля."""
        return (self._screen_width - self.board_lenght * self.getSizeCell()) // 2,\
               (self._screen_height - self.board_lenght * self.getSizeCell()) // 2

    def getSizeCell(self):
        """Размер одной клетки = размер png файла."""
        return 64

