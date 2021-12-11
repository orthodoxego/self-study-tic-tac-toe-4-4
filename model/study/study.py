from random import choice, randint
from dataclasses import dataclass

@dataclass
class TemplateInfo:
    template: str = "нет шаблона."
    chars: str = "нет строки."
    count: int = 0

class Study:
    """Организация записи ходов и анализа текущего хода."""

    def __init__(self, field, setup):
        self.field = field
        self.setup = setup
        self.file = setup.dataset_file_name

        self.__old_count_dataset = 0

        self.info_template = TemplateInfo()
        self.dataset = self.readDataAll()
        self.workspace = []
        # Для дампа для записи в датасет (выгружает каждые 50 записей)
        self.saved_dump = []
        self.initialize()

        self.digit = ""
        for i in range(65, 65 + setup.board_lenght ** 2):
            self.digit += chr(i)

    def log(self, s):
        print(s)
        pass

    def initialize(self):
        """Инициализация в начале каждого раунда."""
        self.__current_game = ""
        self.workspace.clear()
        self.workspace = self.dataset[:]
        self.info_template.count = len(self.workspace)

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

        self.info_template.count = len(result)
        return result

    def saveDataAll(self, end=False):
        if not self.setup.save_data:
            return False

        if self.__current_game != "":
            last = f"{self.setup.figure01}{self.setup.figure02}{self.setup.clear_field}"
            if self.__current_game[-1] in last:
                if not (self.__current_game in self.dataset):
                    self.saved_dump.insert(0, self.__current_game)
                    self.dataset.insert(0, self.__current_game)
                    self.__old_count_dataset += 1

        if len(self.saved_dump) > 50 or end:
            try:
                f = open(self.file, "w", encoding="UTF-8")
                for i in range(len(self.dataset)):
                    f.write(self.dataset[i] + "\n")
                f.close()
                print(f"Дамп датасета выгружен ({len(self.dataset)} записей) / Новых: ({self.__old_count_dataset})")
                self.saved_dump.clear()
                self.__old_count_dataset = 0
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

    def getNextMove(self, figure_win, figure_lose, field):
        """Вычисляет позицию по датасету."""
        result = {"X": -1, "Y": -1, "DATA": figure_win}

        wins_move = []
        draw_move = []
        lose_move = []
        current_string = self.__current_game

        if self.setup.learn_bot:
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
        if len(wins_move) > 0:
            worker_dataset = choice(wins_move)
            self.info_template.chars = f"{worker_dataset}"
            self.info_template.template = "Победа"
        elif len(draw_move) > 0:
            if self.setup.draw_game:
                worker_dataset = choice(draw_move)
                self.info_template.chars = f"{worker_dataset}"
                self.info_template.template = "Ничья"
        else:
            self.info_template.chars = f"-"
            self.info_template.template = "Нет шаблона"

        if len(current_string) <= 1 and randint(0, 100) < 70:
            # xT = 1 + randint(0, self.setup.board_lenght // 4)
            # yT = 1 + randint(0, self.setup.board_lenght // 4)
            xT = self.setup.board_lenght // 2
            yT = self.setup.board_lenght // 2
            if field[xT][yT] == self.setup.clear_field:
                result["X"] = xT
                result["Y"] = yT
        elif worker_dataset != None:
            copy_field = [f[:] for f in field]
            # Поиск хода-завершения
            coord = self.getAttackMove(figure_win, copy_field)
            if coord != None:
                result["X"] = coord["X"]
                result["Y"] = coord["Y"]
            else:
                coord = self.getXYFromChar(worker_dataset[max(0, len(current_string))])
                result["X"] = coord[0]
                result["Y"] = coord[1]
        else:
            copy_field = [f[:] for f in field]
            # Поиск хода-завершения
            coord = self.getAttackMove(figure_win, copy_field)
            if coord != None:
                result["X"] = coord["X"]
                result["Y"] = coord["Y"]
            else:
                # Поиск хода-защиты
                coord = self.getDefendMove(figure_lose, copy_field)
                if coord != None:
                    result["X"] = coord["X"]
                    result["Y"] = coord["Y"]
                else:
                    coord = self.getSecondAttackMove(figure_win, copy_field)
                    if coord != None:
                        result["X"] = coord["X"]
                        result["Y"] = coord["Y"]

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


        # Если не найдено, то найти соседствующую клетку слева или справа от фигуры
        if len(choice_cells) == 0:
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

        # Если до сих пор не найдена подходящая клетка, то добавить случайную
        if len(choice_cells) == 0:
            for x in range(len(field)):
                for y in range(len(field[x])):
                    if field[x][y] == self.setup.clear_field:
                        choice_cells.append([x, y])

        final_cell = choice(choice_cells)
        ret["X"] = final_cell[0]
        ret["Y"] = final_cell[1]

        return ret

    def getSecondAttackMove(self, figure, field):
        """Вернёт клетку для вторичной атаки. Формат: словарь {"X": x, "Y", y}"""
        coord = {"X": None, "Y": None}

        pr = self.getSupposition(".X.X.", figure, field)
        if pr != None:
            coord["X"] = pr[1][0]
            coord["Y"] = pr[1][1]
            return coord

        pr = self.getSupposition("XX..", figure, field)
        if pr != None:
            coord["X"] = pr[1][0]
            coord["Y"] = pr[1][1]
            return coord

        return None

    def getAttackMove(self, figure, field):
        """Вернёт клетку для атаки. Формат: словарь {"X": x, "Y", y}"""
        coord = {"X": None, "Y": None}
                  # Предполагаемый ход
        pr = self.getSupposition(".XXX", figure, field)
        if pr != None:
            coord["X"] = pr[0][0]
            coord["Y"] = pr[0][1]
            return coord

        pr = self.getSupposition("X.XX", figure, field)
        if pr != None:
            coord["X"] = pr[0][0]
            coord["Y"] = pr[0][1]
            return coord

        return None

    def getDefendMove(self, figure, field):
        """Вернёт клетку для защиты. Формат: словарь {"X": x, "Y", y}"""
        coord = {"X": None, "Y": None}
                  # Предполагаемый ход
        pr = self.getSupposition(".XXX", figure, field)
        if pr != None:
            coord["X"] = pr[0][0]
            coord["Y"] = pr[0][1]
            return coord

        pr = self.getSupposition("X.XX", figure, field)
        if pr != None:
            coord["X"] = pr[0][0]
            coord["Y"] = pr[0][1]
            return coord

        pr = self.getSupposition("X.X", figure, field)
        if pr != None:
            coord["X"] = pr[0][0]
            coord["Y"] = pr[0][1]
            return coord

        pr = self.getSupposition("XX..", figure, field)
        if pr != None:
            coord["X"] = pr[0][0]
            coord["Y"] = pr[0][1]
            return coord

        return None

    def getSupposition(self, template, figure, field) -> list:

        # Поиск по вертикали относительно изображения
        for h in range(len(field)):
            for w in range(len(field[h]) - len(template) + 1):
                r = self.getTemplate(h, w, template, figure, field, offcetX=0, offcetY=1, count=0)
                if len(r) > 0:
                    return r

        # Поиск по горизонтали относительно изображения
        for w in range(len(field)):
            for h in range(len(field[h]) - len(template) + 1):
                r = self.getTemplate(h, w, template, figure, field, offcetX=1, offcetY=0, count=0)
                if len(r) > 0:
                    return r

        # Поиск по диагонали сверху-вправо относительно изображения
        for h in range(len(field) - len(template) + 1):
            for w in range(len(field[h]) - len(template) + 1):
                r = self.getTemplate(h, w, template, figure, field, offcetX=1, offcetY=1, count=0)
                if len(r) > 0:
                    return r

        # Поиск по диагонали сверху-влево относительно изображения
        for h in range(len(field) - len(template) + 1):
            for w in range(len(field[h]) - len(template) + 1, len(field[h])):
                r = self.getTemplate(h, w, template, figure, field, offcetX=1, offcetY=-1, count=0)
                if len(r) > 0:
                    return r

        return None

    def getTemplate(self, x, y, template, figure, field, offcetX, offcetY, count) -> list:
        result = []

        r = True
        i = 0
        while i < len(template) and r:
            if template[i] == "X" and field[x + i * offcetX][y + i * offcetY] != figure:
                r = False
            elif template[i] == "." and field[x + i * offcetX][y + i * offcetY] == self.setup.clear_field:
                result.append([x + i * offcetX, y + i * offcetY])
            elif template[i] == "." and field[x + i * offcetX][y + i * offcetY] != self.setup.clear_field:
                r = False
            i += 1

        if not r:
            result.clear()
        if len(result) == 0 and count == 0:
            return self.getTemplate(x, y, template[::-1], figure, field, offcetX, offcetY, count + 1)

        return result