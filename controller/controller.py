class Controller:

    def __init__(self):
        self.mouse_position_x = 0
        self.mouse_position_y = 0
        self.PRESSED_LEFT_KEY_MOUSE = 100
        self.UNPRESSED_LEFT_KEY_MOUSE = 101

    def act(self, pygame, delta):
        return self.check_events(pygame, delta)

    def pressLKM(self):
        """Пользователь нажал ЛКМ."""
        return self.PRESSED_LEFT_KEY_MOUSE

    def unpressLKM(self):
        """Пользователь отпустил ЛКМ."""
        return self.UNPRESSED_LEFT_KEY_MOUSE

    def eventQUIT(self):
        """Закрытие окна."""
        return False

    def pressESCAPE(self):
        """Пользователь нажал Escape."""
        return False

    """Клавиши влево, вправо и так далее."""
    def pressLEFT(self):
        return True

    def pressRIGHT(self):
        return True

    def pressUP(self):
        return True

    def pressDOWN(self):
        return True

    def pressP(self):
        return True

    @property
    def mouse_x(self):
        return self.mouse_position_x

    @property
    def mouse_y(self):
        return self.mouse_position_y

    def check_events(self, pygame, delta):
        result = True

        self.mouse_position_x = pygame.mouse.get_pos()[0]
        self.mouse_position_y = pygame.mouse.get_pos()[1]

        for event in pygame.event.get():

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    return self.pressLKM()

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    return self.unpressLKM()

            # Закрыли окно
            elif event.type == pygame.QUIT:
                result *= self.eventQUIT()

            # Клавиши
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    result *= self.pressESCAPE()
                elif event.key == pygame.K_LEFT:
                    result *= self.pressLEFT()
                elif event.key == pygame.K_RIGHT:
                    result *= self.pressRIGHT()
                elif event.key == pygame.K_UP:
                    result *= self.pressUP()
                elif event.key == pygame.K_DOWN:
                    result *= self.pressDOWN()
                elif event.key == pygame.K_p or event.key == pygame.K_PAUSE:
                    result *= self.pressP()

        return result

class ControllerGame(Controller):

    def __init__(self):
        super().__init__()


