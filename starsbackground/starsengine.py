import random

from starsbackground.star import Star
from random import randint, choice

class StarsEngine:
    """Движок для звёзд."""

    def __init__(self, count_star, screen_width, screen_height):
        colors = ((150, 200, 250),
                  (150, 150, 175),
                  (100, 100, 100))

        self.__stars = []
        for i in range(count_star):
            x = random.randint(0, screen_width)
            y = random.randint(0, screen_height)
            speed_x = -screen_width // randint(150, 255)
            color = choice(colors)
            self.__stars.append(Star(x, y, speed_x, 0, color))

        Star.screen_width = screen_width
        Star.screen_height = screen_height

    def act(self, delta):
        for star in self.__stars:
            star.act(delta)

    def draw(self, pygame, scene):
        for star in self.__stars:
            star.draw(pygame, scene)
