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
        self.__type_game = ["Бот VS Бот", "Бот VS Игрок", "Игрок VS Бот", "Игрок VS Игрок"]
        self.__type_game_number = 0
        if self.setup.config_game == 1:
            self.__type_game_number = 1
        elif self.setup.config_game == 10:
            self.__type_game_number = 2
        elif self.setup.config_game == 11:
            self.__type_game_number = 3

        self.__size_game = ["4x4", "5x5", "7x7", "9x9"]
        self.__size_game_number = 0

        self.__menu = []
        self.__menu.append(MenuData("Начать игру", self.setup.screen_width // 4,
                                    100,
                                    self.setup.screen_width // 1.5, 60))
        self.__menu.append(MenuData("Тип игры: " + self.__type_game[self.__type_game_number],
                                    self.setup.screen_width // 4,
                                    150, self.setup.screen_width // 1.5, 60))
        self.__menu.append(MenuData("Размер поля: " + self.__size_game[self.__size_game_number],
                                    self.setup.screen_width // 4,
                                    200, self.setup.screen_width // 1.5, 60))


        self.__menu.append(MenuData("Прекратить вакханалию...", self.setup.screen_width // 4, 550, self.setup.screen_width // 1.5, 60))


        self.__select_item = -1

    def act(self, pygame, delta):
        ret = self.__controller.check_events(pygame, delta)

        # Проверяет реакцию на пункты меню
        if ret == 100:
            if self.__select_item == 0:
                pygame.mouse.set_visible(True)
                return 10
            if self.__select_item == len(self.__menu) - 1:
                return 27
            # Тип игры
            if self.__select_item == 1:
                self.__type_game_number += 1
                if self.__type_game_number >= len(self.__type_game):
                    self.__type_game_number = 0
                self.__menu[self.__select_item].text = "Тип игры: " + self.__type_game[self.__type_game_number]
                if self.__type_game_number == 0:
                    self.setup.config_game = 0
                elif self.__type_game_number == 1:
                    self.setup.config_game = 1
                elif self.__type_game_number == 2:
                    self.setup.config_game = 10
                elif self.__type_game_number == 3:
                    self.setup.config_game = 11

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

        for i in range(len(self.__menu)):
            if i == 0:
                scene.blit(self.__font.getBigText("MENU" + str(i), self.__menu[i].text, self.setup.GREEN), (self.__menu[i].x, self.__menu[i].y))
            elif i == len(self.__menu) - 1:
                scene.blit(self.__font.getBigText("MENU" + str(i), self.__menu[i].text, self.setup.RED),
                           (self.__menu[i].x, self.__menu[i].y))
            else:
                scene.blit(self.__font.getBigText("MENU" + str(i), self.__menu[i].text, self.setup.GRAY),
                           (self.__menu[i].x, self.__menu[i].y))

        scene.blit(self.__cursor, (
        self.__controller.mouse_x - self.__correct_cursor_x, self.__controller.mouse_y - self.__correct_cursor_y))

