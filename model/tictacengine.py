import pygame.time

from controller.controller import ControllerGame
from model.services.playermove import PlayerMove
from model.services.gamestate import GameState
from model.services.services import Services
from setup import Setup
from model.datamodel import DataModel
from view.textures import Textures
from view.textview import TextView
from view.view import View


class TicTacEngine:
    """Игровой движок. Включает и организует взаимодействие всего со всем."""
    def __init__(self):
        self.setup = Setup()
        self.textures = Textures()
        self.__datamodel = DataModel()
        self.__view = View(self.textures)
        self.__text = TextView()
        self.__controller = ControllerGame()
        self.__services = Services(self.setup.start_point_x, self.setup.start_point_y)
        self.__gamestate = GameState.PLAYER

        # Объекты-обработчики действий игрока
        self.__playerMove = PlayerMove()

    def contfoller(self, pygame, delta):
        result_controller = True

        result_controller *= self.__controller.act(pygame, delta)

        if self.__gamestate == GameState.PLAYER:
            # Нажата левая кнопка мыши
            if result_controller == self.__controller.PRESSED_LEFT_KEY_MOUSE:
                self.playerMove()
        elif self.__gamestate == GameState.BOT:
            self.__gamestate = GameState.PLAYER

        return result_controller

    def act(self, pygame, delta):
        result_act = True

        return result_act

    def draw(self, scene, clock):

        # Отрисует активную клетку в зависимости от курсора мыши
        xy = self.__services.getPositionSelectedCells(self.__controller.mouse_x, self.__controller.mouse_y, self.setup)
        draw_selected_cell_x = xy[0]
        draw_selected_cell_y = xy[1]

        # Отрисует игровую модель: поле, фигуры и выделенную плитку
        self.__view.draw_cells_and_figure(scene, self.__datamodel.field, draw_selected_cell_x, draw_selected_cell_y)
        self.__view.draw_texture(scene, 10, 10, self.__text.getSystemText("FPS", f"FPS: {int(clock.get_fps())}", self.setup.GREEN))

    def playerMove(self):

        xy_pressed_cells = self.__services.getCellsCoord(self.__controller.mouse_x, self.__controller.mouse_y,
                                                         self.setup)
        x = xy_pressed_cells[0]
        y = xy_pressed_cells[1]
        print(xy_pressed_cells, f"Number: {y * self.setup.board_lenght + x}")

        self.__gamestate = self.__playerMove.getMove(xy_pressed_cells, self.__datamodel.field,
                                                     GameState.BOT,
                                                     GameState.PLAYER,
                                                     self.setup.figure01)