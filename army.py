from dataclasses import dataclass

import pygame

from unit import Unit


@dataclass()
class Army:
    banner: pygame.Surface

    def __init__(self, banner, pos_x, pos_y, units, money) -> None:
        self.banner = pygame.image.load(banner).convert_alpha()
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.units = units
        self.money = money

    def move(self, x, y):
        self.pos_x = x
        self.pos_y = y
        self.units[0].pos_x = x
        self.units[0].pos_y = y

    def recruitUnit(self, army, gridSize):
        if army == "A":
            self.units.append(Unit(0, 0, 1000, 50, 'images/blueUnit.png'))
        else:
            self.units.append(Unit(gridSize - 1, gridSize - 1, 1000, 50, 'images/redUnit.png'))
        self.money -= 1000
