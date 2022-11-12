import numpy as np
import pygame


def drawGrid(screen, grid, w_width, w_height):
    army_A_color = pygame.Color(255, 150, 150)
    army_B_color = pygame.Color(150, 150, 255)
    neutral_color = (255, 255, 255)

    size = grid.size
    blockSize = (min(w_width, w_height) - size) / size

    for x in range(0, size):
        for y in range(0, size):
            pos_x = (blockSize + 1) * x
            pos_y = (blockSize + 1) * y
            rect = pygame.Rect(pos_x, pos_y, blockSize, blockSize)
            # Draw cells
            if grid.grid[x][y] == 1:
                pygame.draw.rect(screen, army_A_color, rect, 0)
            elif grid.grid[x][y] == 2:
                pygame.draw.rect(screen, army_B_color, rect, 0)
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
    pygame.display.flip()


class Grid:
    def __init__(self, size, armyA, armyB):
        self.size = size
        self.grid = np.zeros((size, size))
        self.armyA = armyA
        self.armyB = armyB

    # TODO
    def update(self):
        pass
