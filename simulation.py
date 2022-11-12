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

    blit(screen, timer, grid, w_width, w_height, armyA, armyB)

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
                blit(screen, timer, grid, w_width, w_height, armyA, armyB)
        pygame.display.flip()
    pygame.quit()


def blit(screen, timer, grid, w_width, w_height, armyA, armyB):
    drawGrid(screen, grid, w_width, w_height)
    screen.fill((128, 128, 128), rect=(670, 100, 50, 50))
    screen.fill((128, 128, 128), rect=(670, 130, 100, 50))
    screen.fill((128, 128, 128), rect=(670, 160, 100, 50))
    font = pygame.font.SysFont('Garamond', 16)
    timerSurface = font.render("Day: " + str(timer), False, (255, 0, 0))
    armyA_Surface = font.render("Gold army A: " + str(armyA.money), False, (212, 175, 55))
    armyB_Surface = font.render("Gold army B: " + str(armyB.money), False, (212, 175, 55))
    screen.blit(timerSurface, (650, 100))
    screen.blit(armyA_Surface, (650, 130))
    screen.blit(armyB_Surface, (650, 160))
