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

    font = pygame.font.SysFont('Garamond', 16)
    # Set background
    screen.fill((128, 128, 128))
    textSurface = font.render("Day: " + str(timer), False, (255, 0, 0))
    screen.blit(textSurface, (700, 100))

    armyA = Army('images/redArmy.png', 0, 0, 1, 100)
    armyB = Army('images/blueArmy.png', gridSize - 1, gridSize - 1, 1, 100)

    grid = Grid(gridSize, armyA, armyB)
    grid.grid[0][0].occupied_by = 1
    grid.grid[gridSize - 1][gridSize - 1].occupied_by = 2

    drawGrid(screen, grid, w_width, w_height)

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
                drawGrid(screen, grid, w_width, w_height)
                screen.fill((128, 128, 128), rect=(720, 100, 50, 50))
                textSurface = font.render("Day: " + str(timer), False, (255, 0, 0))
                screen.blit(textSurface, (700, 100))
        pygame.display.flip()
    pygame.quit()
