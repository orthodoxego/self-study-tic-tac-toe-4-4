from setup import Setup
from random import randint

class DataModel:

    def __init__(self):
        self.setup = Setup()
        self.initizlizeField()

    def initizlizeField(self):
        self.__field = [[self.setup.clear_field for i in range (self.setup.board_lenght)]
                      for j in range(self.setup.board_lenght)]

        # self.setUserField()

    def setUserField(self):
        a = self.setup.figure01
        b = self.setup.figure02
        c = self.setup.clear_field

        self.__field = [[c, c, c, c, c],
                        [c, c, a, a, c],
                        [c, c, c, c, c],
                        [c, c, c, c, c],
                        [c, c, c, c, c]]

    @property
    def field(self):
        return self.__field


