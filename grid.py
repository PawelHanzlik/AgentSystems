import random

import numpy as np
import pygame

from field import Field


def drawGrid(screen, grid, w_width, w_height):
    army_A_color = pygame.Color(150, 150, 255)
    army_B_color = pygame.Color(255, 150, 150)
    neutral_color = (255, 255, 255)

    size = grid.size
    blockSize = (min(w_width, w_height) - size) / size

    for x in range(0, size):
        for y in range(0, size):
            pos_x = (blockSize + 1) * x
            pos_y = (blockSize + 1) * y
            rect = pygame.Rect(pos_x, pos_y, blockSize, blockSize)
            # Draw cells
            if grid.grid[x][y].occupied_by == 1:
                pygame.draw.rect(screen, army_A_color, rect, 0)
            elif grid.grid[x][y].occupied_by == 2:
                pygame.draw.rect(screen, army_B_color, rect, 0)
                grid.grid[x][y].occupied_by = 2
            else:
                pygame.draw.rect(screen, neutral_color, rect, 0)

            if grid.armyA.pos_x == x and grid.armyA.pos_y == y:
                # Draw armyA
                armyA_img = grid.armyA.banner
                armyA_img = pygame.transform.scale(armyA_img, (blockSize, blockSize))
                screen.blit(armyA_img, rect)

            if grid.armyB.pos_x == x and grid.armyB.pos_y == y:
                # Draw armyB
                armyB_img = grid.armyB.banner
                armyB_img = pygame.transform.scale(armyB_img, (blockSize, blockSize))
                screen.blit(armyB_img, rect)

    for (i, unit) in enumerate(grid.armyA.units):
        if i != 0 and unit not in grid.armyA.units_merged:
            unitA_img = pygame.transform.scale(unit.image, (blockSize, blockSize))
            screen.blit(unitA_img, pygame.Rect(unit.pos_x*(blockSize+1), unit.pos_y*(blockSize+1), blockSize, blockSize))
    for (i, unit) in enumerate(grid.armyB.units):
        if i != 0 and unit not in grid.armyB.units_merged:
            unitB_img = pygame.transform.scale(unit.image, (blockSize, blockSize))
            screen.blit(unitB_img, pygame.Rect(unit.pos_x*(blockSize+1), unit.pos_y*(blockSize+1), blockSize, blockSize))
    pygame.display.flip()


class Grid:
    def __init__(self, size, armyA, armyB):
        self.size = size
        self.grid = np.array(
            [[Field(i, j, int(random.random() * 10 + 1), 0) for i in range(size)] for j in range(size)])
        self.armyA = armyA
        self.armyB = armyB

    def update(self):
        self.grid[self.armyA.pos_x][self.armyA.pos_y].occupied_by = 1
        self.grid[self.armyB.pos_x][self.armyB.pos_y].occupied_by = 2

        # TODO
        newAfield = random.choice(self.neighbours(self.armyA.pos_x, self.armyA.pos_y))
        newBfield = random.choice(self.neighbours(self.armyB.pos_x, self.armyB.pos_y))

        self.armyA.move(newAfield[0], newAfield[1])
        self.armyB.move(newBfield[0], newBfield[1])

        for u in self.armyA.units:
            m = random.choice(self.neighbours(u.pos_x, u.pos_y))
            u.move(m[0], m[1])
            if u.pos_x == self.armyA.pos_x and u.pos_y == self.armyA.pos_y and u not in self.armyA.units_merged:
                self.armyA.units_merged.append(u)

        for u in self.armyB.units:
            m = random.choice(self.neighbours(u.pos_x, u.pos_y))
            u.move(m[0], m[1])
            if u.pos_x == self.armyB.pos_x and u.pos_y == self.armyB.pos_y and u not in self.armyB.units_merged:
                self.armyB.units_merged.append(u)

        if self.armyA.money > 1000:
            self.armyA.recruitUnit("A", self.size)
        if self.armyB.money > 1000:
            self.armyB.recruitUnit("B", self.size)
        self.updateTreasure()

    def neighbours(self, row, col):
        neighbours = flatten([[(i, j) if 0 <= i < len(self.grid) and 0 <= j < len(self.grid[0]) else ()
                               for i in range(row - 1, row + 2)]
                              for j in range(col - 1, col + 2)])
        return neighbours

    def updateTreasure(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.grid[i][j].occupied_by == 1:
                    self.armyA.money += self.grid[i][j].gold_generated
                if self.grid[i][j].occupied_by == 2:
                    self.armyB.money += self.grid[i][j].gold_generated
        for unit in self.armyA.units:
            self.armyA.money -= unit.maintenance
        for unit in self.armyB.units:
            self.armyB.money -= unit.maintenance
        if self.armyA.money < 0:
            self.armyA.money = 0
        if self.armyB.money < 0:
            self.armyB.money = 0


def flatten(_):
    return [item for sublist in _ for item in sublist if item != ()]
