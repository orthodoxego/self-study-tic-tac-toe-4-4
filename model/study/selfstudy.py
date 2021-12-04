from random import choice

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
        self.workspace = self.dataset[:]

    def readDataAll(self):
        result = []
        try:
            f = open(self.file, "r", encoding="UTF-8")
            result = f.readlines()
            f.close()
            for i in range(len(result)):
                result[i] = result[i].replace("\n", "")
        except:
            f = open(self.file, "w", encoding="UTF-8")
            f.close()
        return result

    def saveDataAll(self):
        if self.__current_game != "":
            last = f"{self.setup.figure01}{self.setup.figure02}{self.setup.clear_field}"
            if self.__current_game[-1] in last:
                if not (self.__current_game in self.dataset):
                    self.dataset.insert(0, self.__current_game)
        try:
            f = open(self.file, "w", encoding="UTF-8")
            for i in range(len(self.dataset)):
                f.write(self.dataset[i] + "\n")
            f.close()
            return True
        except:
            print("Невозможно сохранить файл.")
        return False

    def addWin(self, winning):
        self.__current_game += f",{winning}"

    def addStep(self, x, y):
        numberCells = y * self.setup.board_lenght + x
        self.__current_game += self.getChar(numberCells)

    def getChar(self, n):
        return self.digit[n]

    def getXYFromChar(self, ch):
        """Вернёт позиции X и Y в зависимости от номера символа."""
        numberCell = self.digit.find(ch)
        return (numberCell % self.setup.board_lenght, numberCell // self.setup.board_lenght)

    def getNextMove(self, figure_win, figure_lose):
        """Вычисляет позицию по датасету."""
        result = {"X": -1, "Y": -1, "DATA": figure_win}

        wins_move = []
        draw_move = []
        lose_move = []
        current_string = self.__current_game

        for data_set in self.workspace:
            if len(current_string) != 0:
                if current_string == data_set[0:len(current_string)]:
                    if data_set[-1] == str(figure_win):
                        wins_move.append(data_set)
                    elif data_set[-1] == str(self.setup.clear_field):
                        draw_move.append(data_set)
                    elif data_set[-1] == str(figure_lose):
                        lose_move.append(data_set)
            else:
                if data_set[-1] == str(figure_win):
                    wins_move.append(data_set)
                elif data_set[-1] == str(self.setup.clear_field):
                    draw_move.append(data_set)
                elif data_set[-1] == str(figure_lose):
                    lose_move.append(data_set)

        worker_dataset = None
        # if len(wins_move) != 0:
        #    worker_dataset = choice(wins_move)
        #elif len(draw_move) != 0:
        #   worker_dataset = choice(draw_move)

        if worker_dataset != None:
            coord = self.getXYFromChar(worker_dataset[max(0, len(current_string))])
            result["X"] = coord[0]
            result["Y"] = coord[1]

        self.workspace.clear()
        if len(wins_move) > 0:
            self.workspace += wins_move
        if len(draw_move) > 0:
            self.workspace += draw_move
        if len(lose_move) > 0:
            self.workspace += lose_move

        result["DATA"] = figure_win

        return result

    def getSegment(self, figure, field):
        """Вернёт случайную свободную позицию рядом с существующей клеткой."""
        ret = {"X": -1, "Y": -1}

        choice_cells = []

        for x in range(len(field)):
            for y in range(len(field[x])):
                if field[x][y] == figure:
                    if x - 1 >= 0:
                        if field[x - 1][y] == self.setup.clear_field:
                            choice_cells.append([x - 1, y])
                    if x + 1 < self.setup.board_lenght:
                        if field[x + 1][y] == self.setup.clear_field:
                            choice_cells.append([x + 1, y])
                    if y + 1 < self.setup.board_lenght:
                        if field[x][y + 1] == self.setup.clear_field:
                            choice_cells.append([x, y + 1])
                    if y - 1 >= 0:
                        if field[x][y - 1] == self.setup.clear_field:
                            choice_cells.append([x, y - 1])
                    if x + 1 < self.setup.board_lenght and y + 1 < self.setup.board_lenght:
                        if field[x + 1][y + 1] == self.setup.clear_field:
                            choice_cells.append([x + 1, y + 1])
                    if x - 1 >= 0 and y + 1 < self.setup.board_lenght:
                        if field[x - 1][y + 1] == self.setup.clear_field:
                            choice_cells.append([x - 1, y + 1])
                    if x - 1 >= 0 and y - 1 >= 0:
                        if field[x - 1][y - 1] == self.setup.clear_field:
                            choice_cells.append([x - 1, y - 1])
                    if x + 1 < self.setup.board_lenght and y - 1 >= 0:
                        if field[x + 1][y - 1] == self.setup.clear_field:
                            choice_cells.append([x + 1, y - 1])


        for x in range(len(field)):
            for y in range(len(field[x])):
                if field[x][y] == self.setup.clear_field:
                    choice_cells.append([x, y])

        final_cell = choice(choice_cells)
        ret["X"] = final_cell[0]
        ret["Y"] = final_cell[1]

        return ret