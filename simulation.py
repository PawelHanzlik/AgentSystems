import pygame

from pygame.locals import (
    # K_UP,
    # K_DOWN,
    # K_LEFT,
    K_RIGHT,
    # K_ESCAPE,
    KEYDOWN,
    QUIT,
)

from army import Army
from grid import Grid, drawGrid


def simulation():

    pygame.init()
    # Parameters
    w_width = 800
    w_height = 600
    gridSize = 30

    # Set up the drawing window, adjust the size
    screen = pygame.display.set_mode([w_width, w_height])

    armyA = Army('images/redArmy.png', 0, 0, 1, 100)
    armyB = Army('images/blueArmy.png', gridSize - 1, gridSize - 1, 1, 100)

    grid = Grid(gridSize, armyA, armyB)
    grid.grid[0][0].occupied_by = 1
    grid.grid[gridSize - 1][gridSize - 1].occupied_by = 2
    for i in range(gridSize):
        for j in range(gridSize):
            print(grid.grid[i][j])
    # Set background
    screen.fill((128, 128, 128))

    drawGrid(screen, grid, w_width, w_height)

    running = True

    time_delay = 1000
    timer_event = pygame.USEREVENT + 1
    pygame.time.set_timer(timer_event, time_delay)

    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

            if event.type == KEYDOWN:
                if event.key == K_RIGHT:
                    grid.update()
                    drawGrid(screen, grid, w_width, w_height)
            if event.type == timer_event:
                grid.update()
                drawGrid(screen, grid, w_width, w_height)

    pygame.quit()
