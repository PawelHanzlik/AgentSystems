import numpy as np
import pygame


def drawGrid(screen, grid, w_width, w_height):
    army_A_color = (255, 0, 0)
    army_B_color = (0, 0, 255)
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
            else:
                pygame.draw.rect(screen, neutral_color, rect, 0)
    pygame.display.flip()


class Grid:
    def __init__(self, size):
        self.size = size
        self.grid = np.zeros((size, size))

    # TODO
    def update(self):
        pass
