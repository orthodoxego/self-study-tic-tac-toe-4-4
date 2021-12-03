import pygame.time

from controller.controller import ControllerGame
from model.services.playermove import PlayerMove
from model.services.gamestate import GameState
from model.services.services import Services
from model.study.selfstudy import SelfStudy
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
        self.__game_state = GameState.PLAYER

        # Класс-обучалка
        self.study = SelfStudy(self.__datamodel.field, self.setup)

        # Результат игры
        self.__result_game = None

        # Объекты-обработчики действий игрока
        self.__playerMove = PlayerMove()
        self.__botMove = PlayerMove()

    def contfoller(self, pygame, delta):
        result_controller = True

        result_controller *= self.__controller.act(pygame, delta)

        if self.__game_state == GameState.PLAYER:
            # Нажата левая кнопка мыши
            if result_controller == self.__controller.PRESSED_LEFT_KEY_MOUSE:
                self.runMove(self.playerOneMove())

        if self.__game_state == GameState.BOT:
            if result_controller == self.__controller.PRESSED_LEFT_KEY_MOUSE:
                self.runMove(self.playerTwoMove())

        if not result_controller:
            self.study.saveDataAll()

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

    def playerOneMove(self):

        xy_pressed_cells = self.__services.getCellsCoord(self.__controller.mouse_x, self.__controller.mouse_y,
                                                         self.setup)

        new_state = self.__playerMove.getMove(xy_pressed_cells, self.__datamodel.field,
                                                     GameState.BOT,
                                                     GameState.PLAYER,
                                                     self.setup.figure01)

        if new_state != self.__game_state:
            self.study.addStep(xy_pressed_cells[0], xy_pressed_cells[1])

        return new_state

    def playerTwoMove(self):
        xy_pressed_cells = self.__services.getCellsCoord(self.__controller.mouse_x, self.__controller.mouse_y,
                                                         self.setup)
        new_state = self.__playerMove.getMove(xy_pressed_cells, self.__datamodel.field,
                                                     GameState.PLAYER,
                                                     GameState.BOT,
                                                     self.setup.figure02)
        if new_state != self.__game_state:
            self.study.addStep(xy_pressed_cells[0], xy_pressed_cells[1])

        return new_state

    def winGame(self):
        res = self.__services.getWinningCells(self.__datamodel.field, self.setup)
        print(res)
        return res

    def runMove(self, current_user_function):
        new_state = current_user_function
        if new_state != self.__game_state:
            self.__result_game = self.winGame()
            if self.__result_game["WIN"] == self.setup.clear_field:
                self.__game_state = new_state
            else:
                self.__game_state = GameState.WINGAME
