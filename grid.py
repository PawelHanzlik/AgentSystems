import math
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
                drawArmy(screen, grid.armyA, blockSize, rect)

            if grid.armyB.pos_x == x and grid.armyB.pos_y == y:
                drawArmy(screen, grid.armyB, blockSize, rect)

    allUnitsDraw(screen, grid.armyA, blockSize)
    allUnitsDraw(screen, grid.armyB, blockSize)

    pygame.display.flip()

def drawArmy(screen, army, blockSize, rect):
    army_img = army.banner
    army_img = pygame.transform.scale(army_img, (blockSize, blockSize))
    screen.blit(army_img, rect)

def allUnitsDraw(screen, army, blockSize):
    for (i, unit) in enumerate(army.units):
        if i != 0 and unit not in army.units_merged:
            unit_img = pygame.transform.scale(unit.image, (blockSize, blockSize))
            screen.blit(unit_img,
                        pygame.Rect(unit.pos_x * (blockSize + 1), unit.pos_y * (blockSize + 1), blockSize, blockSize))

def advanceToArmy(neighbours, army):
    nearest = math.dist(neighbours[0], (army.pos_x, army.pos_y))
    nearest_i = 0
    for (i, n) in enumerate(neighbours):
        if math.dist(n, (army.pos_x, army.pos_y)) < nearest:
            nearest = math.dist(n, (army.pos_x, army.pos_y))
            nearest_i = i
    return neighbours[nearest_i]


def updateMorale(army, flag):
    if flag == 1:
        army.morale += 0.4
    else:
        army.morale -= 0.4
    round(army.morale, 2)

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
        if not self.armyA.in_battle:
            newAfield = random.choice(self.neighbours(self.armyA.pos_x, self.armyA.pos_y))
            newBfield = random.choice(self.neighbours(self.armyB.pos_x, self.armyB.pos_y))

            self.armyA.move(newAfield[0], newAfield[1])
            self.armyB.move(newBfield[0], newBfield[1])

        self.allUnitsMove(self.armyA)
        self.allUnitsMove(self.armyB)

        self.checkRecruitmentPossibility(self.armyA, "A")
        self.checkRecruitmentPossibility(self.armyB, "B")
        self.updateTreasure()

        if self.armyA.pos_x == self.armyB.pos_x and self.armyA.pos_y == self.armyB.pos_y:
            self.armyA.in_battle = True
            self.armyB.in_battle = True

    def allUnitsMove(self, army):
        for u in army.units:
            m = advanceToArmy(self.neighbours(u.pos_x, u.pos_y), army)
            u.move(m[0], m[1])
            if u.pos_x == army.pos_x and u.pos_y == army.pos_y and \
                    u.identifier not in [unit.identifier for unit in army.units_merged]:
                army.units_merged.append(u)
                updateMorale(army, 1)

    def checkRecruitmentPossibility(self, army, ab):
        if army.money > 1000:
            army.recruitUnit(ab, self.size)
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
        if self.armyA.money < -100:
            if len(self.armyA.units) == len(self.armyA.units_merged):
                self.armyA.units.pop()
                self.armyA.units_merged.pop()
                updateMorale(self.armyA, 0)
        if self.armyB.money < -100:
            if len(self.armyB.units) == len(self.armyB.units_merged):
                self.armyB.units.pop()
                self.armyB.units_merged.pop()
                updateMorale(self.armyB, 0)


def flatten(_):
    return [item for sublist in _ for item in sublist if item != ()]
