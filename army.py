from dataclasses import dataclass

import pygame


@dataclass()
class Army:
    banner: pygame.Surface

    def __init__(self, banner, pos_x, pos_y, units, money) -> None:
        self.banner = pygame.image.load(banner).convert_alpha()
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.units = units
        self.money = money
