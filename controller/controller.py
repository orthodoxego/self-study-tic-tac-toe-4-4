from setup import Setup

class Controller:

    def __init__(self):
        self.lkm_pressed = False
        self.__pause = False

    @property
    def pause(self):
        return self.__pause

    @pause.setter
    def pause(self, value):
        self.__pause = value

    def __invertPause(self):
        self.lkm_pressed = False
        self.__pause = not self.__pause

    def act(self, pygame, delta):
        return self.__check_events(pygame, delta)

    def __check_events(self, pygame, delta):

        for event in pygame.event.get():

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and not self.pause:
                    self.lkm_pressed = True
                return True

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.lkm_pressed = False
                return True

            # Закрыли окно
            elif event.type == pygame.QUIT:
                return False

            # Клавиши
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                elif event.key == pygame.K_LEFT:
                    pass
                elif event.key == pygame.K_RIGHT:
                    pass
                elif event.key == pygame.K_UP:
                    pass
                elif event.key == pygame.K_DOWN:
                    pass
                elif event.key == pygame.K_p or event.key == pygame.K_PAUSE:
                    self.__invertPause()

        return True
