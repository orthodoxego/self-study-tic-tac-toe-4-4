class Services:

    def __init__(self, start_point_x, start_point_y):
        self.start_point_x = start_point_x
        self.start_point_y = start_point_y

    def getPositionSelectedCells(self, x, y, setup):
        """Вернёт координаты для отрисовки выделенной клетки в
        зависимости от позиции курсора мыши."""
        correct_for_center_mouse = setup.getSizeCell() // 2
        if self.start_point_x < x < self.start_point_x + setup.board_lenght * setup.getSizeCell() \
                and self.start_point_y < y < self.start_point_y + setup.board_lenght * setup.getSizeCell():
            return_x = (x + correct_for_center_mouse) // setup.getSizeCell() * setup.getSizeCell() - correct_for_center_mouse
            return_y = (y + correct_for_center_mouse) // setup.getSizeCell() * setup.getSizeCell() - correct_for_center_mouse
            return (return_x, return_y)
        else:
            return (-setup.getSizeCell(), -setup.getSizeCell())

    def getCellsCoord(self, mouse_x, mouse_y, setup):
        correct_for_center_mouse = setup.getSizeCell() // 2
        mouse_x -= self.start_point_x
        mouse_y -= self.start_point_y

        return_x = (mouse_x // setup.getSizeCell()) % setup.getSizeCell()
        return_y = (mouse_y // setup.getSizeCell()) % setup.getSizeCell()

        return (return_x, return_y)

    def getWinningCells(self, field, setup):
        """Определяет, выграл ли игрок.
        В случае выигрыша возвращает кортеж с координатами клеток-победителей и номером победителя."""
        winCells = []
        res = {"WIN": setup.clear_field, "CELLS": winCells}

        # Маркера фигур для поиска в поле
        figures = f"{setup.figure01}{setup.figure02}{setup.clear_field}"

        # Маркера для фигур первого игрока и условного противника
        player = figures[0] * 4
        enemy = figures[1] * 4

        # Поиск совпадений
        for i in range(len(field)):
            horizontal = ""
            vertical = ""
            for j in range(len(field)):
                horizontal += figures[field[j][i]]
                vertical += figures[field[i][j]]

            win = None
            if player in horizontal:
                win = player
            elif enemy in horizontal:
                win = enemy

            if win != None:
                res["WIN"] = int(win[0])
                for o in range(horizontal.find(win[0]), horizontal.find(win[0]) + 4):
                    winCells.append((i, o))
                res["CELLS"] = tuple(winCells)
                return res

            win = None
            if player in vertical:
                win = player
            elif enemy in vertical:
                win = enemy

            if win != None:
                res["WIN"] = int(win[0])
                for o in range(vertical.find(win[0]), vertical.find(win[0]) + 4):
                    winCells.append((o, i))
                res["CELLS"] = tuple(winCells)
                return res


        res["CELLS"] = tuple(res["CELLS"])
        return res
