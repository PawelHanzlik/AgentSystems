import pygame


class Unit:

    def __init__(self, identifier, pos_x, pos_y, cost, maintenance, image) -> None:
        self.identifier = identifier
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.cost = cost
        self.maintenance = maintenance
        self.image = pygame.image.load(image).convert_alpha()

    def move(self, x, y):
        self.pos_x = x
        self.pos_y = y

    def __str__(self) -> str:
        return f"({self.pos_x},{self.pos_y}) -> cost: {self.cost}"
