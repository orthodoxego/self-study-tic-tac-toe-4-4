from controller.controller import ControllerGameMenu
from menu.menudata import MenuData
from view.font import Font
from view.textures import Textures

class GameMenu:
    """Главное меню игры."""

    def __init__(self, pygame, setup):
        self.setup = setup
        self.__cursor = Textures().figure[0]
        self.__correct_cursor_x = self.__cursor.get_width() // 2
        self.__correct_cursor_y = self.__cursor.get_height() // 2
        self.__controller = ControllerGameMenu()
        self.__font = Font()

        pygame.mouse.set_visible(False)

        # ========== Пункты меню ==========
        self.__type_game = [["Бот VS Бот", 0], ["Бот VS Игрок", 1], ["Игрок VS Бот", 10], ["Игрок VS Игрок", 11]]
        self.__type_game_number = 0
        for i in range(len(self.__type_game)):
            if self.setup.config_game == self.__type_game[i][1]:
                self.__type_game_number = i

        self.__size_game = [["4x4", 4], ["5x5", 5], ["6x6", 6], ["7x7", 7], ["9x9", 9], ["12x12", 12]]
        self.__size_game_number = 0
        for i in range(len(self.__size_game)):
            if self.setup.board_lenght == self.__size_game[i][1]:
                self.__size_game_number = i

        self.__pause_round_game = [["щелчок мыши", 0], ["0.01 сек.", 0.01], ["0.5 сек.", 0.5], ["1 сек.", 1], ["2 сек.", 2], ["3 сек.", 3]]
        self.__pause_round_game_number = 0
        for i in range(len(self.__pause_round_game)):
            if self.setup.pause_round == self.__pause_round_game[i][1]:
                self.__pause_round_game_number = i

        self.__save_dataset = [["игнорировать", False], ["записывать в датасет", True]]
        self.__save_dataset_number = self.setup.save_data

        self.__learn_bot = [["игнорят (глупее)", False], ["пользуются (умнее)", True]]
        self.__learn_bot_number = self.setup.learn_bot

        self.__draw_bot = [["нет", False], ["да", True]]
        self.__draw_bot_number = self.setup.draw_game

        self.__save_dataset = [["игнорировать", False], ["записывать в датасет", True]]
        self.__save_dataset_number = self.setup.save_data

        self.__fps = [30, 60, 120, 180, 240, 300]
        self.__fps_number = 0
        for i in range(len(self.__fps)):
            if setup.FPS == self.__fps[i]:
                self.__fps_number = i


        self.__menu = []
        left_border = int(self.setup.screen_width * 0.2)
        width_menu = int(self.setup.screen_width * 0.78)
        self.__menu.append(MenuData("Начать игру", left_border,
                                    100,
                                    width_menu, 60))
        self.__menu.append(MenuData("Тип игры: " + self.__type_game[self.__type_game_number][0],
                                    left_border,
                                    200, width_menu, 60))
        self.__menu.append(MenuData("Размер поля: " + self.__size_game[self.__size_game_number][0],
                                    left_border,
                                    250, width_menu, 60))
        self.__menu.append(MenuData("Пауза между раундами: " + self.__pause_round_game[self.__pause_round_game_number][0],
                                    left_border,
                                    300, width_menu, 60))
        self.__menu.append(MenuData("Новые комбинации: " + self.__save_dataset[self.__save_dataset_number][0],
                                    left_border,
                                    350, width_menu, 60))

        self.__menu.append(MenuData("Боты и датасет: " + str(self.__learn_bot[self.__learn_bot_number][0]),
                                    left_border,
                                    400, width_menu, 60))

        self.__menu.append(MenuData("Включать комбинации с \"ничьей\": " + str(self.__draw_bot[self.__draw_bot_number][0]),
                                    left_border,
                                    450, width_menu, 60))

        self.__menu.append(MenuData("Стремиться к FPS: " + str(self.__fps[self.__fps_number]),
                                    left_border,
                                    500, width_menu, 60))


        self.__menu.append(MenuData("Прекратить вакханалию...",
                                    left_border,
                                    600,
                                    width_menu, 60))


        self.__select_item = -1

    def act(self, pygame, delta):
        ret = self.__controller.check_events(pygame, delta)

        if ret == 100:
            ret = self.menuReaction()

        if ret == 10 or ret == 27:
            pygame.mouse.set_visible(True)
            self.setup.saveSettings()

        mx = self.__controller.mouse_x
        my = self.__controller.mouse_y

        self.__menu_select_x, self.__menu_select_y = -1, -1

        # Находит координаты для подсветки
        for i in range(len(self.__menu)):
            mnu = self.__menu[i]
            if mx > mnu.x and mx < mnu.x + mnu.width and my > mnu.y and my < mnu.y + mnu.heigth:
                self.__select_item = i

        return ret

    def draw(self, pygame, scene):
        if self.__select_item >= 0:
            mnu = self.__menu[self.__select_item]
            pygame.draw.rect(scene, self.setup.ULTRAMARINE, (mnu.x - mnu.width // 10, mnu.y - mnu.heigth // 5, mnu.width, mnu.heigth))
            pygame.draw.rect(scene, self.setup.LIGHT_BLUE, (mnu.x - mnu.width // 10, mnu.y - mnu.heigth // 5, mnu.width, mnu.heigth), 1)
            pygame.draw.rect(scene, self.setup.BLUE, (mnu.x - mnu.width // 10 + 3, mnu.y - mnu.heigth // 5 + 3, mnu.width - 6, mnu.heigth - 6), 1)

        for i in range(len(self.__menu)):
            if i == 0:
                scene.blit(self.__font.getBigText("MENU" + str(i), self.__menu[i].text, self.setup.GREEN), (self.__menu[i].x, self.__menu[i].y))
            elif i == len(self.__menu) - 1:
                scene.blit(self.__font.getBigText("MENU" + str(i), self.__menu[i].text, self.setup.RED),
                           (self.__menu[i].x, self.__menu[i].y))
            else:
                scene.blit(self.__font.getBigText("MENU" + str(i), self.__menu[i].text, self.setup.GRAY),
                           (self.__menu[i].x, self.__menu[i].y))


        if self.__select_item > 0 and self.__select_item < len(self.__menu) - 1:
            scene.blit(self.__font.getBigText("MENU" + str(i), self.__menu[self.__select_item].text, self.setup.LIGHT_BLUE),
                       (self.__menu[self.__select_item].x, self.__menu[self.__select_item].y))



        scene.blit(self.__cursor, (self.__controller.mouse_x - self.__correct_cursor_x,
                                   self.__controller.mouse_y - self.__correct_cursor_y))

    def menuReaction(self):
        # Проверяет реакцию на пункты меню
        if self.__select_item == 0:
            return 10
        if self.__select_item == len(self.__menu) - 1:
            return 27
        # Тип игры
        if self.__select_item == 1:
            self.__type_game_number += 1
            if self.__type_game_number >= len(self.__type_game):
                self.__type_game_number = 0
            self.__menu[self.__select_item].text = "Тип игры: " + self.__type_game[self.__type_game_number][0]
            self.setup.config_game = self.__type_game[self.__type_game_number][1]

        # Размер поля
        elif self.__select_item == 2:
            self.__size_game_number += 1
            if self.__size_game_number >= len(self.__size_game):
                self.__size_game_number = 0
            self.__menu[self.__select_item].text = "Размер поля: " + self.__size_game[self.__size_game_number][0]
            self.setup.board_lenght = self.__size_game[self.__size_game_number][1]
            self.setup.setStartPoint()

        # Пауза между раундами
        elif self.__select_item == 3:
            self.__pause_round_game_number += 1
            if self.__pause_round_game_number >= len(self.__pause_round_game):
                self.__pause_round_game_number = 0
            self.__menu[self.__select_item].text = "Пауза между раундами: " + \
                                                   self.__pause_round_game[self.__pause_round_game_number][0]
            self.setup.pause_round = self.__pause_round_game[self.__pause_round_game_number][1]

        # Комбинации в датасет
        elif self.__select_item == 4:
            self.__save_dataset_number += 1
            if self.__save_dataset_number >= len(self.__save_dataset):
                self.__save_dataset_number = 0
            self.__menu[self.__select_item].text = "Новые комбинации: " + \
                                                   self.__save_dataset[self.__save_dataset_number][0]
            self.setup.save_data = self.__save_dataset[self.__save_dataset_number][1]

        # Использование датасета
        elif self.__select_item == 5:
            self.__learn_bot_number += 1
            if self.__learn_bot_number >= len(self.__learn_bot):
                self.__learn_bot_number = 0
            self.__menu[self.__select_item].text = "Боты и датасет: " + str(self.__learn_bot[self.__learn_bot_number][0])
            self.setup.learn_bot = self.__learn_bot[self.__learn_bot_number][1]

        # Комбинации с ничьей
        elif self.__select_item == 6:
            self.__draw_bot_number += 1
            if self.__draw_bot_number >= len(self.__draw_bot):
                self.__draw_bot_number = 0
            self.__menu[self.__select_item].text = "Включать комбинации с \"ничьей\": " + str(self.__draw_bot[self.__draw_bot_number][0])
            self.setup.draw_game = self.__draw_bot[self.__draw_bot_number][1]


        # ФПС
        elif self.__select_item == 7:
            self.__fps_number += 1
            if self.__fps_number >= len(self.__fps):
                self.__fps_number = 0
            self.__menu[self.__select_item].text = "Стремиться к FPS: " + str(self.__fps[self.__fps_number])
            self.setup.FPS = self.__fps[self.__fps_number]