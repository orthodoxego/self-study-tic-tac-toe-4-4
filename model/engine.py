import copy

import pygame.time

from controller.controller import ControllerGame
from model.services.playermove import PlayerMove
from model.services.gamestate import GameState
from model.services.services import Services
from model.study.selfstudy import SelfStudy
from setup import Setup
from model.datamodel import DataModel
from view.textures import Textures
from view.font import Font
from view.view import View


class TicTacEngine:
    """Игровой движок. Включает и организует взаимодействие всего со всем."""

    def __init__(self):
        self.setup = Setup()
        self.textures = Textures()
        self.__datamodel = DataModel()
        self.__view = View(self.textures)
        self.__text = Font()
        self.__controller = ControllerGame()
        self.__services = Services(self.setup.start_point_x, self.setup.start_point_y)
        self.default_state = GameState.PLAYER

        # Класс-обучалка
        self.study = SelfStudy(self.__datamodel.field, self.setup)

        # Объекты-обработчики действий игрока
        self.__player_move = PlayerMove()
        self.__bot_move = PlayerMove()
        self.__move_function = {GameState.BOT: self.playerTwoMove,
                                GameState.PLAYER: self.playerOneMove}
        self.__count_win_player_and_bot = [0, 0]

        self.restartGame()

    def restartGame(self):
        """Новый раунд."""
        self.__datamodel.initizlizeField()
        self.__game_state = self.default_state
        self.study.initialize()
        self.__count_frame = 0

        # Результат игры
        self.__result_game = None

    def controller(self, pygame, delta):
        result_controller = True

        result_controller *= self.__controller.act(pygame, delta)

        if self.__game_state == GameState.WINGAME or self.__game_state == GameState.DRAWGAME:
            if self.setup.pause_per_round == 0:
                if result_controller == self.__controller.PRESSED_LEFT_KEY_MOUSE:
                    self.restartGame()
            else:
                if self.__count_frame > self.setup.FPS * self.setup.pause_per_round:
                    self.restartGame()
        else:
            # Отрабатывает ход игрока или бота
            if self.setup.learn:
                if self.__count_frame % max(1, self.setup.pause_frame_per_bot) == 0:
                    self.runBotMove(self.__game_state)
            else:
                if result_controller == self.__controller.PRESSED_LEFT_KEY_MOUSE:
                    self.runMove(self.__move_function[self.__game_state]())

        if not result_controller:
            self.study.saveDataAll()

        return result_controller

    def act(self, pygame, delta):
        result_act = True

        self.__count_frame += 1
        if self.__count_frame > self.setup.FPS * 100:
            self.__count_frame = 0

        return result_act

    def draw(self, scene, clock):

        # Системные сообщения
        # ФПС
        self.__view.draw_texture(scene, 10, 10,
                                 self.__text.getSystemText("FPS", f"FPS: {int(clock.get_fps())}", self.setup.GREEN))
        self.__view.draw_texture(scene, 10, 45,
                                 self.__text.getSystemText("COUNT_WIN_1", f"Игрок 1: {self.__count_win_player_and_bot[0]}", self.setup.RED))
        self.__view.draw_texture(scene, 10, 70,
                                 self.__text.getSystemText("COUNT_WIN_2", f"Игрок 2: {self.__count_win_player_and_bot[1]}", self.setup.LIGHT_BLUE))

        # Состояние игры при победе или ничье
        if self.__game_state == GameState.WINGAME or self.__game_state == GameState.DRAWGAME:
            self.draw_win_or_draw_game(scene)
        else:
            # Отрисует активную клетку в зависимости от курсора мыши
            xy = self.__services.getPositionSelectedCells(self.__controller.mouse_x, self.__controller.mouse_y, self.setup)
            draw_selected_cell_x = xy[0]
            draw_selected_cell_y = xy[1]

            # Отрисует игровую модель: поле, фигуры и выделенную плитку
            self.__view.draw_cells_and_figure(scene, self.__datamodel.field, draw_selected_cell_x, draw_selected_cell_y)

    def playerOneMove(self):
        xy_pressed_cells = self.__services.getCellsCoord(self.__controller.mouse_x, self.__controller.mouse_y,
                                                         self.setup)

        new_state = self.__player_move.getMove(xy_pressed_cells, self.__datamodel.field,
                                               GameState.BOT,
                                               GameState.PLAYER,
                                               self.setup.figure01)

        if new_state != self.__game_state:
            self.study.addStep(xy_pressed_cells[0], xy_pressed_cells[1])

        return new_state

    def playerTwoMove(self):
        xy_pressed_cells = self.__services.getCellsCoord(self.__controller.mouse_x, self.__controller.mouse_y,
                                                         self.setup)
        new_state = self.__player_move.getMove(xy_pressed_cells, self.__datamodel.field,
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

    def checkDrawGame(self, field):
        # Самое коряво написанное, но быстрое копирование в Python

        for_player = [x[:] for x in field]

        for i in range(len(for_player)):
            for j in range(len(for_player[i])):
                if for_player[i][j] == self.setup.clear_field:
                    for_player[i][j] = self.setup.figure01

        res = self.__services.getWinningCells(for_player, self.setup)
        if res["WIN"] != self.setup.clear_field * 20:
            return False

        for_enemy = [x[:] for x in field]
        for i in range(len(for_enemy)):
            for j in range(len(for_enemy[i])):
                if for_enemy[i][j] == self.setup.clear_field:
                    for_enemy[i][j] = self.setup.figure02

        res = self.__services.getWinningCells(for_enemy, self.setup)
        if res["WIN"] == self.setup.clear_field * 20:
            self.study.addWin(self.setup.clear_field)
            self.study.saveDataAll()
            self.__game_state = GameState.DRAWGAME

        return True


    def runMove(self, current_user_function):
        """Проверка выигрышной или ничейной позиции, на основе которой смена состояния игры."""
        new_state = current_user_function
        if new_state != self.__game_state:
            self.__result_game = self.winGame()
            if self.__result_game["WIN"] == self.setup.clear_field * 20:
                self.__game_state = new_state
                self.checkDrawGame(self.__datamodel.field)
            else:
                self.study.addWin(self.__result_game["WIN"])
                self.study.saveDataAll()
                #print(self.__result_game["WIN"])
                self.__count_win_player_and_bot[int(self.__result_game["WIN"])] += 1
                self.__count_frame = 0
                self.__game_state = GameState.WINGAME

    def runBotMove(self, state):
        if self.__game_state == GameState.PLAYER:
            self.study.getNextMove(self.setup.figure02)
        else:
            self.study.getNextMove(self.setup.figure01)

    def draw_win_or_draw_game(self, scene):
        if self.__game_state == GameState.WINGAME:
            txt = self.__text.getBigText("WIN_TEXT", f"Игра закончена. Счёт: {self.__count_win_player_and_bot[0]}:{self.__count_win_player_and_bot[1]}",
                                            self.setup.GREEN)
            self.__view.draw_texture(scene, (self.setup.screen_width - txt.get_width()) // 2,
                                     self.setup.screen_height - txt.get_height() * 4, txt)
        else:
            txt = self.__text.getBigText("DRAW_TEXT",
                                         f"Ничья. Счёт: {self.__count_win_player_and_bot[0]}:{self.__count_win_player_and_bot[1]}",
                                         self.setup.YELLOW)
            self.__view.draw_texture(scene, (self.setup.screen_width - txt.get_width()) // 2,
                                     self.setup.screen_height - txt.get_height() * 4, txt)


        self.__view.draw_win_cells(scene, self.__datamodel.field, self.__result_game)
        if self.setup.pause_per_round == 0:
            txt = self.__text.getSystemText("PRESS_LKM", f"Нажмите левую кнопку мыши для продолжения.",
                                            self.setup.YELLOW)
            self.__view.draw_texture(scene, (self.setup.screen_width - txt.get_width()) // 2,
                                     self.setup.screen_height - txt.get_height() * 2, txt)
        else:
            txt = self.__text.getSystemText("NEXT_LEVEL",
                                            f"Новый раунд... {1 + (self.setup.pause_per_round * self.setup.FPS - self.__count_frame) // 60}",
                                            self.setup.YELLOW)
            self.__view.draw_texture(scene, (self.setup.screen_width - txt.get_width()) // 2,
                                     self.setup.screen_height - txt.get_height() * 2, txt)
