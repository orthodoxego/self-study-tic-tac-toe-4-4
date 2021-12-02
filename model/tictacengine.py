from controller.controller import Controller

class TicTacEngine:

    def __init__(self):
        self.__controller = Controller()


    def act(self, pygame, delta):
        return self.__controller.act(pygame, delta)

    def draw(self, scene, delta):
        pass