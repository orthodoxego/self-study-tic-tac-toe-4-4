from setup import Setup

class View:

    def __init__(self, textures):
        self.setup = Setup()
        self.__texture = textures

    def draw_texture(self, scene, x, y, texture):
        scene.blit(texture, (x, y))

    def draw_cells(self, i, j, scene, x_select, y_select, texture_select):
        """Отрисовка игрового поля из цикла в обычной текстуре или выделенного."""
        x = self.setup.start_point_x + i * self.setup.getSizeCell()
        y = self.setup.start_point_y + j * self.setup.getSizeCell()
        if x == x_select and y == y_select:
            scene.blit(texture_select, (x, y))
        else:
            scene.blit(self.__texture.cell, (x, y))

    def draw_cells_and_figure(self, scene, data, x_select, y_select):
        """Построение игрового поля и отрисовка фигур."""
        for i in range(self.setup.board_lenght):
            for j in range(self.setup.board_lenght):
                texture_select = self.__texture.cell_select
                if data[i][j] != self.setup.clear_field:
                    texture_select = self.__texture.cell_district

                self.draw_cells(i, j, scene, x_select, y_select, texture_select)

                if data[i][j] != self.setup.clear_field:
                    scene.blit(self.__texture.figure[data[i][j]], (self.setup.start_point_x + i * self.setup.getSizeCell(),
                                                     self.setup.start_point_y + j * self.setup.getSizeCell()))

    def draw_win_cells(self, scene, data, result_game):
        """Построение игрового поля, когда игра закончена. Отрисовка фигур."""
        win_pos = result_game["CELLS"]
        for i in range(self.setup.board_lenght):
            for j in range(self.setup.board_lenght):
                x = self.setup.start_point_x + i * self.setup.getSizeCell()
                y = self.setup.start_point_y + j * self.setup.getSizeCell()
                texture = self.__texture.cell
                if (j, i) in win_pos:
                    texture = self.__texture.cell_win
                scene.blit(texture, (x, y))

                if data[i][j] != self.setup.clear_field:
                    scene.blit(self.__texture.figure[data[i][j]], (x, y))
