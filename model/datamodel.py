from setup import Setup
from random import randint

class DataModel:

    def __init__(self):
        self.setup = Setup()
        # self.__field = [[randint(0, 1) for i in range (self.setup.board_lenght)]
        self.__field = [[self.setup.clear_field for i in range (self.setup.board_lenght)]
                      for j in range(self.setup.board_lenght)]

    @property
    def field(self):
        return self.__field
