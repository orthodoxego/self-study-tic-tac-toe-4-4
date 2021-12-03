class SelfStudy:
    """Организация записи ходов и анализа текущего хода."""
    def __init__(self, field, setup):
        self.field = field
        self.setup = setup
        self.file = setup.dataset_file_name

        self.dataset = self.readDataAll()
        self.workspace = []
        self.initialize()

        self.digit = ""
        for i in range(65, 65 + setup.board_lenght ** 2):
            self.digit += chr(i)


    def initialize(self):
        """Инициализация в начале каждого раунда."""
        self.__current_game = ""
        self.workspace.clear()

    def addStep(self, x, y):
        numberCells = y * self.setup.board_lenght + x
        self.__current_game += self.getChar(numberCells)
        print(self.__current_game)

    def getChar(self, n):
        return self.digit[n]

    def readDataAll(self):
        result = []
        try:
            f = open(self.file, "r", encoding="UTF-8")
            result = f.readlines()
            f.close()
        except:
            f = open(self.file, "w", encoding="UTF-8")
            f.close()
        return result

    def saveDataAll(self):
        if self.__current_game != "":
            last = f"{self.setup.figure01}{self.setup.figure02}{self.setup.clear_field}"
            if self.__current_game[-1] in last:
                self.__current_game += "\n"
                if not (self.__current_game in self.dataset):
                    self.dataset.insert(0, self.__current_game)
        try:
            f = open(self.file, "w", encoding="UTF-8")
            for i in range(len(self.dataset)):
                f.write(self.dataset[i])
            f.close()
            return True
        except:
            print("Невозможно сохранить файл.")
        return False

    def addWin(self, winning):
        self.__current_game += f",{winning}"