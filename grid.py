import math
import random

import numpy as np
import pygame

from field import Field
from unit import Unit


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

            for a in grid.kingdomA.armies:
                if a.pos_x == x and a.pos_y == y:
                    drawArmy(screen, a, blockSize, rect)
            for b in grid.kingdomB.armies:
                if b.pos_x == x and b.pos_y == y:
                    drawArmy(screen, b, blockSize, rect)

    for a in grid.kingdomA.armies:
        allUnitsDraw(screen, a, blockSize)
    for b in grid.kingdomB.armies:
        allUnitsDraw(screen, b, blockSize)

    pygame.display.flip()


def drawArmy(screen, army, blockSize, rect):
    army_img = army.banner
    army_img = pygame.transform.scale(army_img, (blockSize, blockSize))
    screen.blit(army_img, rect)


def allUnitsDraw(screen, army, blockSize):
    for (i, unit) in enumerate(army.units):
        if unit not in army.units_merged:
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


def updateMoraleBattle(army):
    army.morale -= random.random() / 5
    if army.morale < 0:
        army.morale = 0
    round(army.morale, 2)


def reviveMorale(army):
    army.morale = 1.5
    for i in range(1, len(army.units_merged)):
        army.morale += 0.4
    round(army.morale, 2)


def inflictLosses(army, lost, x, y, ab):
    if lost:
        if ab == "A":
            army.units = []
            army.units_merged = [Unit(1, x, y, 0, 5, 'images/blueUnit.png')]
        else:
            army.units = []
            army.units_merged = [Unit(1, x, y, 0, 5, 'images/redUnit.png')]
    else:
        for i in range(len(army.units_merged) // 2):
            army.units_merged.pop(-1)


def retreat(armyLost, armyWon, x, y, ab):
    armyLost.in_battle = False
    armyWon.in_battle = False
    armyLost.pos_x = x
    armyLost.pos_y = y
    armyLost.money = 0
    armyWon.money = 0
    inflictLosses(armyLost, True, x, y, ab)
    inflictLosses(armyWon, False, x, y, ab)
    reviveMorale(armyLost)
    reviveMorale(armyWon)


class Grid:
    def __init__(self, size, kingdomA, kingdomB):
        self.size = size
        self.grid = np.array(
            [[Field(i, j, int(random.random() * 10 + 1), 1) if i < size // 2 and j < size // 2 else
              Field(i, j, int(random.random() * 10 + 1), 0) for i in range(size)] for j in range(size)])
        self.grid[0, 0].standing_on.append(kingdomA.armies[0])
        self.grid[size - 1, size - 1].standing_on.append(kingdomB.armies[0])
        self.kingdomA = kingdomA
        self.kingdomB = kingdomB

    def update(self):
        self.checkRecruitmentPossibility("A")
        self.checkRecruitmentPossibility("B")

        if len(self.kingdomA.armies) > len(self.kingdomB.armies):
            for i in range(len(self.kingdomA.armies)):
                if i < len(self.kingdomB.armies):
                    self.updateArmyA(self.kingdomA.armies[i])
                    self.updateArmyB(self.kingdomB.armies[i])
                else:
                    self.updateArmyA(self.kingdomA.armies[i])

        elif len(self.kingdomA.armies) < len(self.kingdomB.armies):
            for i in range(len(self.kingdomB.armies)):
                if i < len(self.kingdomA.armies):
                    self.updateArmyA(self.kingdomA.armies[i])
                    self.updateArmyB(self.kingdomB.armies[i])
                else:
                    self.updateArmyB(self.kingdomB.armies[i])
        else:
            for i in range(len(self.kingdomA.armies)):
                self.updateArmyA(self.kingdomA.armies[i])
                self.updateArmyB(self.kingdomB.armies[i])

        self.kingdomA.morale -= 0.01
        self.kingdomB.morale -= 0.01
        if sum(len(army.units) + len(army.units_merged) for army in self.kingdomA.armies) < 5:
            self.kingdomA.morale -= 0.1
        if sum(len(army.units) + len(army.units_merged) for army in self.kingdomA.armies) / \
                sum(len(army.units) + len(army.units_merged) for army in self.kingdomB.armies) > 3 and \
                sum(len(army.units) + len(army.units_merged) for army in self.kingdomA.armies) > 50:
            self.kingdomB.morale -= 0.2
        if sum(len(army.units) + len(army.units_merged) for army in self.kingdomB.armies) / \
                sum(len(army.units) + len(army.units_merged) for army in self.kingdomA.armies) > 3 and \
                sum(len(army.units) + len(army.units_merged) for army in self.kingdomB.armies) > 50:
            self.kingdomA.morale -= 0.2
        if sum(len(army.units) + len(army.units_merged) for army in self.kingdomB.armies) < 5:
            self.kingdomB.morale -= 0.1
        self.updateTreasure()

    def updateArmyA(self, armyA):
        self.grid[armyA.pos_x][armyA.pos_y].occupied_by = 1
        self.allUnitsMove(armyA, "A")

        if not armyA.in_battle:
            newAfield = self.armyMove(armyA)
            if armyA in self.grid[armyA.pos_x][armyA.pos_y].standing_on:
                self.grid[armyA.pos_x][armyA.pos_y].standing_on.remove(armyA)
            armyA.move(newAfield[0], newAfield[1])
            self.grid[newAfield[0], newAfield[1]].standing_on.append(armyA)
        else:
            if armyA.morale == 0:
                retreat(armyA, armyA.opponent, 0, 0, "A")
                self.kingdomA.morale -= 0.7
                self.kingdomB.morale += 0.3
            else:
                updateMoraleBattle(armyA)

        for i in range(len(self.grid[armyA.pos_x, armyA.pos_y].standing_on)):
            if self.grid[armyA.pos_x, armyA.pos_y].standing_on[i].number != armyA.number:
                armyA.in_battle = True
                armyA.opponent = self.grid[armyA.pos_x, armyA.pos_y].standing_on[i]

    def updateArmyB(self, armyB):
        self.grid[armyB.pos_x][armyB.pos_y].occupied_by = 2
        self.allUnitsMove(armyB, "B")

        if not armyB.in_battle:
            newAfield = self.armyMove(armyB)
            if armyB in self.grid[armyB.pos_x][armyB.pos_y].standing_on:
                self.grid[armyB.pos_x][armyB.pos_y].standing_on.remove(armyB)
            armyB.move(newAfield[0], newAfield[1])
            self.grid[newAfield[0], newAfield[1]].standing_on.append(armyB)
        else:
            if armyB.morale == 0:
                retreat(armyB, armyB.opponent, len(self.grid) - 1, len(self.grid[0]) - 1, "B")
                self.kingdomB.morale -= 0.7
                self.kingdomA.morale += 0.3
            else:
                updateMoraleBattle(armyB)

        for i in range(len(self.grid[armyB.pos_x, armyB.pos_y].standing_on)):
            if self.grid[armyB.pos_x, armyB.pos_y].standing_on[i].number != armyB.number:
                armyB.in_battle = True
                armyB.opponent = self.grid[armyB.pos_x, armyB.pos_y].standing_on[i]

    def armyMove(self, army):
        neighbours = self.neighbours(army.pos_x, army.pos_y)
        if army.number == 1 and random.random() < 0.2:
            move = neighbours[-1]
        elif army.number == 2 and random.random() < 0.2:
            move = neighbours[0]
        else:
            move = random.choice(neighbours)

        for i in range(0, len(neighbours)):
            move = self.determineMovement(army, neighbours, i, move)

        return move

    def determineMovement(self, army, neighbours, i, move):
        occupied = self.grid[move].occupied_by

        if neighbours[i][0] == army.pos_x and neighbours[i][1] == army.pos_y:
            return move

        if self.grid[neighbours[i]].occupied_by == 0:
            if (occupied == 0 and self.grid[neighbours[i]].gold_generated > self.grid[move].gold_generated) or (
                    occupied != 0 and occupied != army.number and
                    self.grid[neighbours[i]].gold_generated > self.grid[move].gold_generated * 2) or \
                    (occupied != 0 and occupied == army.number and
                     self.grid[neighbours[i]].gold_generated > self.grid[move].gold_generated):
                move = neighbours[i]
        elif self.grid[neighbours[i]].occupied_by != 0 and self.grid[neighbours[i]].occupied_by != army.number:
            if (occupied == 0 and self.grid[neighbours[i]].gold_generated * 2 > self.grid[move].gold_generated) or (
                    occupied != 0 and occupied != army.number and self.grid[neighbours[i]].gold_generated > self.grid[
                    move].gold_generated):
                move = neighbours[i]
        return move

    def allUnitsMove(self, army, ab):
        to_remove = []
        for u in army.units:
            m = advanceToArmy(self.neighbours(u.pos_x, u.pos_y), army)
            u.move(m[0], m[1])
            if ab == "A":
                if u not in army.units_merged:
                    if army.pos_x == u.pos_x and army.pos_y == u.pos_y:
                        to_remove.append(u)
                        army.units_merged.append(u)
                        updateMorale(army, 1)
                        continue
                    else:
                        self.grid[m[0], m[1]].occupied_by = 1
            else:
                if u not in army.units_merged:
                    if army.pos_x == u.pos_x and army.pos_y == u.pos_y:
                        to_remove.append(u)
                        army.units_merged.append(u)
                        updateMorale(army, 1)
                        continue
                    else:
                        self.grid[m[0], m[1]].occupied_by = 2
        for u in to_remove:
            army.units.remove(u)

    def checkRecruitmentPossibility(self, ab):
        if ab == "A":
            while self.kingdomA.money > 5000:
                self.kingdomA.recruitUnit(ab, self.size)
        elif ab == "B":
            while self.kingdomB.money > 5000:
                self.kingdomB.recruitUnit(ab, self.size)

    def neighbours(self, row, col):
        neighbours = flatten([[(i, j) if 0 <= i < len(self.grid) and 0 <= j < len(self.grid[0]) else ()
                               for i in range(row - 1, row + 2)]
                              for j in range(col - 1, col + 2)])
        return neighbours

    def updateTreasure(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.grid[i][j].occupied_by == 1:
                    self.kingdomA.money += self.grid[i][j].gold_generated
                if self.grid[i][j].occupied_by == 2:
                    self.kingdomB.money += self.grid[i][j].gold_generated
        for army in self.kingdomA.armies:
            for unit in army.units:
                self.kingdomA.money -= unit.maintenance
        for army in self.kingdomB.armies:
            for unit in army.units:
                self.kingdomB.money -= unit.maintenance
        if self.kingdomA.money < -100:
            if len(self.kingdomA.armies[-1].units) == len(self.kingdomA.armies[-1].units_merged):
                self.kingdomA.armies[-1].units.pop()
                self.kingdomA.armies[-1].units_merged.pop()
                updateMorale(self.kingdomA.armies[-1], 0)
        if self.kingdomB.money < -100:
            if len(self.kingdomB.armies[-1].units) == len(self.kingdomB.armies[-1].units_merged):
                self.kingdomB.armies[-1].units.pop()
                self.kingdomB.armies[-1].units_merged.pop()
                updateMorale(self.kingdomB.armies[-1], 0)


def flatten(_):
    return [item for sublist in _ for item in sublist if item != ()]
