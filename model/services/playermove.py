from setup import Setup


class PlayerMove:
    """Обрабатывает движение игрока."""
    def __init__(self):
        """Обрабатывает щелчок ЛКМ по полю."""
        self.setup = Setup()

    def getMove(self, xy_pressed_cells, field, game_state_next, game_state_current, number_figure):
        """Ставит фигуру в указанную клетку.
        Если индекс в пределах диапазона и клетка имеет признак "пустая".
        """
        x = xy_pressed_cells[0]
        y = xy_pressed_cells[1]

        # Возможно ли поставить фигуру?
        # Если границы в диапазоне списка и поле пустое
        setFigure = 0 <= x < len(field) and 0 <= y < len(field[0]) and field[x][y] == self.setup.clear_field

        if setFigure:
            field[x][y] = number_figure
            return game_state_next

        return game_state_current



