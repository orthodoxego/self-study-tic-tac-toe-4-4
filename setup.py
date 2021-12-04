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

        # Коды конфигурации:
        #  0 - играет бот с ботом
        #  1 - бот с человеком (бот ходит первым)
        # 10 - человек с ботом
        # 11 - человек-человек
        self.configGame = 0

        # Пауза для "обдумывания" хода ботом, в кадрах (FPS = 1 секунда)
        self.pause_frame_per_bot = self.FPS // 2

        # Ширина и высота окна для оконного режима
        self._screen_width = 1024
        self._screen_height = 768

        # Пауза между раундами. 0 - ждать щелчка ЛКМ
        # Если, например, значение 0.5 - то пауза в 0.5 секунды
        self.pause_per_round = 0.05

        # Номера фигур, 0 - бот, 1 - игрок, 2 - пустая клетка
        self.figure01 = 0
        self.figure02 = 1
        # Код чистого поля ВСЕГДА должен быть больше предыдущих
        # В коде он умножается на 20 для определения невыигрышной и не нетральной позиции
        # Умножение на 20 даёт уникальный номер
        self.clear_field = 2

        # Размер доски X * X, но не меньше 4х
        self.__board_lenght = 4
        self.setStartPoint()

        # Файл датасета
        if self.__board_lenght < 10:
            name = "0" + str(self.board_lenght)
        else:
            name = str(self.board_lenght)
        self.dataset_file_name = f"dataset{name}.dat"

        # Цвета
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)
        self.BLUE = (0, 0, 255)
        self.LIGHT_BLUE = (175, 218, 252)
        self.YELLOW = (255, 255, 0)

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

    @property
    def board_lenght(self):
        if self.__board_lenght < 4:
            self.__board_lenght = 4
        return self.__board_lenght


    def setStartPoint(self):
        self.start_point_x, self.start_point_y = self.getStartPoint()

    def getStartPoint(self):
        """Вернёт координату левого верхнего угла игрового поля."""
        return (self._screen_width - self.board_lenght * self.getSizeCell()) // 2,\
               (self._screen_height - self.board_lenght * self.getSizeCell()) // 2

    def getSizeCell(self):
        """Размер одной клетки = размер png файла."""
        return 64

