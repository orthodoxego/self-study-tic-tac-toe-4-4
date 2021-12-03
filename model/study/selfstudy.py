class SelfStudy:
    """Организация записи ходов и анализа текущего хода."""
    def __init__(self, field, setup):
        self.field = field
        self.setup = setup
        self.file = setup.dataset_file_name

        self.dataset = self.readDataAll()
        self.__current_game = ""

    def addStep(self, x, y):
        numberCells = y * self.setup.board_lenght + x
        self.__current_game += self.getChar(numberCells)
        # print(self.__current_game)

    def getChar(self, n):
        digit = "ABCDEFGHIJKLMNOPQRSTUVWXY"
        return digit[n]

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
        self.dataset.insert(0, self.__current_game + "\n")
        try:
            f = open(self.file, "w", encoding="UTF-8")
            for i in range(len(self.dataset)):
                f.write(self.dataset[i])
            f.close()
            return True
        except:
            print("Невозможно сохранить файл.")
        return False