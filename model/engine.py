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

        self.__move_function = {GameState.BOT: self.playerTwoMove,
                                GameState.PLAYER: self.playerOneMove,
                                "TYPE": ["Игрок", "Игрок"]}

        if self.setup.config_game == 10:
            self.__move_function = {GameState.BOT: self.runBotMove,
                                    GameState.PLAYER: self.playerOneMove,
                                    "TYPE": ["Игрок", "БОТ"]}
        elif self.setup.config_game == 1:
            self.__move_function = {GameState.BOT: self.playerTwoMove,
                                    GameState.PLAYER: self.runBotMove,
                                    "TYPE": ["БОТ", "Игрок"]}
        elif self.setup.config_game == 0:
            self.__move_function = {GameState.BOT: self.runBotMove,
                                    GameState.PLAYER: self.runBotMove,
                                    "TYPE": ["БОТ", "БОТ"]}


        self.__count_win_player_and_bot = [0, 0, 0]

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
            if self.setup.pause_round == 0:
                if result_controller == self.__controller.PRESSED_LEFT_KEY_MOUSE:
                    self.restartGame()
            else:
                if self.__count_frame > self.setup.FPS * self.setup.pause_round:
                    self.restartGame()
        elif self.__game_state == GameState.PLAYER or self.__game_state == GameState.BOT:
            if self.__game_state == GameState.PLAYER:
                if self.setup.config_game == 0:
                    if self.__count_frame > self.setup.FPS * self.setup.wait_for_move:
                        self.runMove(self.__move_function[self.__game_state]())
                        self.__count_frame = 0
                elif self.setup.config_game >= 10 and result_controller == self.__controller.PRESSED_LEFT_KEY_MOUSE:
                    self.runMove(self.__move_function[self.__game_state]())
                    self.__count_frame = 0
                elif self.setup.config_game == 1:
                    if self.__count_frame > self.setup.FPS * self.setup.wait_for_move:
                        self.runMove(self.__move_function[self.__game_state]())
                        self.__count_frame = 0

            if self.__game_state == GameState.BOT:
                if self.setup.config_game == 11 or self.setup.config_game == 1:
                    if result_controller == self.__controller.PRESSED_LEFT_KEY_MOUSE:
                        self.runMove(self.__move_function[self.__game_state]())
                        self.__count_frame = 0
                elif self.__count_frame > self.setup.FPS * self.setup.wait_for_move:
                    self.runMove(self.__move_function[self.__game_state]())
                    self.__count_frame = 0


        if not result_controller:
            self.study.saveDataAll()

        return result_controller

    def act(self, pygame, delta):
        result_act = True
        self.__count_frame += 1
        if self.__count_frame > self.setup.FPS * 100:
            self.__count_frame = 0

        return result_act

    def draw_system_messages(self, scene, clock):
        # ФПС
        self.__view.draw_texture(scene, 10, 10,
                                 self.__text.getSystemText("FPS", f"FPS: {int(clock.get_fps())}", self.setup.GREEN))
        self.__view.draw_texture(scene, 10, 70,
                                 self.__text.getSystemText("COUNT_WIN_1",
                                                           f"{self.__move_function['TYPE'][0]}: {self.__count_win_player_and_bot[0]}",
                                                           self.setup.LIGHT_RED))
        self.__view.draw_texture(scene, 10, 100,
                                 self.__text.getSystemText("COUNT_WIN_2",
                                                           f"{self.__move_function['TYPE'][1]}: {self.__count_win_player_and_bot[1]}",
                                                           self.setup.LIGHT_BLUE))
        self.__view.draw_texture(scene, 10, 130,
                                 self.__text.getSystemText("DRAW",
                                                           f"Ничья: {self.__count_win_player_and_bot[2]}",
                                                           self.setup.YELLOW))

        if not self.setup.saveData:
            self.__view.draw_texture(scene, 10, self.setup.screen_height - 30,
                                     self.__text.getSystemText("SAVEDATA",
                                                               "Запись датасета: ВЫКЛ.",
                                                               self.setup.RED))
        else:
            self.__view.draw_texture(scene, 10, self.setup.screen_height - 30,
                                     self.__text.getSystemText("SAVEDATA",
                                                               "Запись датасета: ВКЛ.",
                                                               self.setup.GREEN))

        if self.setup.config_game == 0:

            self.__view.draw_texture(scene, 10, self.setup.screen_height - 50,
                                     self.__text.getSystemText("LEARN",
                                                               "Обучение ботов: ВКЛ.",
                                                               self.setup.GREEN))
            self.__view.draw_texture(scene, self.setup.screen_width // 2.3, self.setup.screen_height - 30,
                                     self.__text.getSystemText("LEARN",
                                                               "В setup.py значение self.config_game = 10, чтобы сыграть с ботом",
                                                               self.setup.YELLOW))


    def draw(self, scene, clock):

        # Системные сообщения
        self.draw_system_messages(scene, clock)

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
        return res

    def checkDrawGame(self, field):

        # Самое коряво написанное, но быстрое копирование в Python
        for_player = [f[:] for f in field]

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
            self.__count_win_player_and_bot[self.setup.clear_field] += 1

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
                self.__count_win_player_and_bot[int(self.__result_game["WIN"])] += 1
                self.__count_frame = 0
                self.__game_state = GameState.WINGAME

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
        if self.setup.pause_round == 0:
            txt = self.__text.getSystemText("PRESS_LKM", f"Нажмите левую кнопку мыши для продолжения.",
                                            self.setup.YELLOW)
            self.__view.draw_texture(scene, (self.setup.screen_width - txt.get_width()) // 2,
                                     self.setup.screen_height - txt.get_height() * 2, txt)
        else:
            txt = self.__text.getSystemText("NEXT_LEVEL",
                                            f"Новый раунд... {1 + (self.setup.pause_round * self.setup.FPS - self.__count_frame) // 60}",
                                            self.setup.YELLOW)
            self.__view.draw_texture(scene, (self.setup.screen_width - txt.get_width()) // 2,
                                     self.setup.screen_height - txt.get_height() * 2, txt)

    def runBotMove(self):
        next_move = {"X": -1, "Y": -1, "DATA": self.setup.figure01}
        result_state = None
        if self.__game_state == GameState.PLAYER:
            next_move = self.study.getNextMove(self.setup.figure01, self.setup.figure02, self.__datamodel.field)
            result_state = GameState.BOT
        elif self.__game_state == GameState.BOT:
            next_move = self.study.getNextMove(self.setup.figure02, self.setup.figure01, self.__datamodel.field)
            result_state = GameState.PLAYER

        x = next_move["X"]
        y = next_move["Y"]

        if x != -1 and y != -1:
            self.__datamodel.field[x][y] = next_move["DATA"]
        else:
            segment = None
            if self.__game_state == GameState.PLAYER:
                segment = self.study.getSegment(self.setup.figure01, self.__datamodel.field)
                x = segment["X"]
                y = segment["Y"]
                self.__datamodel.field[x][y] = self.setup.figure01
            elif self.__game_state == GameState.BOT:
                segment = self.study.getSegment(self.setup.figure02, self.__datamodel.field)
                x = segment["X"]
                y = segment["Y"]
                self.__datamodel.field[x][y] = self.setup.figure02


        self.study.addStep(x, y)

        return result_state

