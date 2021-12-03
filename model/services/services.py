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
