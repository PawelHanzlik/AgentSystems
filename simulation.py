import pygame

from pygame.locals import (
    QUIT
)

from army import Army
from grid import Grid, drawGrid
from unit import Unit


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
    unitsA = [Unit(0, 0, 0, 5, 'images/blueUnit.png')]
    unitsB = [Unit(gridSize - 1, gridSize - 1, 0, 5, 'images/redUnit.png')]
    armyA = Army('images/blueArmy.png', 0, 0, unitsA, 800)
    armyB = Army('images/redArmy.png', gridSize - 1, gridSize - 1, unitsB, 800)

    grid = Grid(gridSize, armyA, armyB)
    grid.grid[0][0].occupied_by = 1
    grid.grid[gridSize - 1][gridSize - 1].occupied_by = 2
    # Set background
    screen.fill((128, 128, 128))

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
