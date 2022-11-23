from dataclasses import dataclass

import pygame

from unit import Unit


@dataclass()
class Army:
    banner: pygame.Surface

    def __init__(self, banner, number, pos_x, pos_y, units, units_merged, money, in_battle, morale) -> None:
        self.banner = pygame.image.load(banner).convert_alpha()
        self.number = number
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.units = units
        self.units_merged = units_merged
        self.money = money
        self.in_battle = in_battle
        self.morale = morale

    def move(self, x, y):
        self.pos_x = x
        self.pos_y = y
        self.units[0].pos_x = x
        self.units[0].pos_y = y

    def recruitUnit(self, army, gridSize):
        if army == "A":
            if self.pos_x != 0 or self.pos_y != 0:
                self.units.append(Unit(len(self.units) + 1, 0, 0, 1000, 30, 'images/blueUnit.png'))
            else:
                self.units.append(Unit(len(self.units) + 1, 1, 0, 1000, 30, 'images/blueUnit.png'))
        else:
            if self.pos_x != 0 or self.pos_y != 0:
                self.units.append(Unit(len(self.units) + 1, gridSize - 1, gridSize - 1, 1000, 30, 'images/redUnit.png'))
            else:
                self.units.append(Unit(len(self.units) + 1, gridSize - 2, gridSize - 1, 1000, 30, 'images/redUnit.png'))
        self.money -= 1000
