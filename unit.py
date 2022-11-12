import pygame


class Unit:

    def __init__(self, pos_x, pos_y, cost, maintenance, image) -> None:
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.cost = cost
        self.maintenance = maintenance
        self.image = pygame.image.load(image).convert_alpha()

    def move(self, x, y):
        self.pos_x = x
        self.pos_y = y
