import pygame

from pygame.locals import (
    QUIT
)

from army import Army
from grid import Grid, drawGrid


def simulation():
    pygame.init()
    timer = 0
    # Parameters
    w_width = 800
    w_height = 600
    gridSize = 30

    # Set up the drawing window, adjust the size
    screen = pygame.display.set_mode([w_width, w_height])

    # Set background
    screen.fill((128, 128, 128))
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

    blit(screen, timer, grid, w_width, w_height)

    running = True

    time_delay = 1000
    timer_event = pygame.USEREVENT + 1
    pygame.time.set_timer(timer_event, time_delay)

    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

            if event.type == timer_event:
                timer += 1
                grid.update()
                blit(screen, timer, grid, w_width, w_height)
        pygame.display.flip()
    pygame.quit()


def blit(screen, timer, grid, w_width, w_height):
    drawGrid(screen, grid, w_width, w_height)
    screen.fill((128, 128, 128), rect=(720, 100, 50, 50))
    font = pygame.font.SysFont('Garamond', 16)
    timerSurface = font.render("Day: " + str(timer), False, (255, 0, 0))
    screen.blit(timerSurface, (700, 100))
