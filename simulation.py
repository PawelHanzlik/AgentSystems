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
    gridSize = 10

    # Set up the drawing window, adjust the size
    screen = pygame.display.set_mode([w_width, w_height])

    # Set background
    screen.fill((128, 128, 128))
    unitsA = [Unit(1, 0, 0, 0, 5, 'images/blueUnit.png')]
    unitsB = [Unit(1, gridSize - 1, gridSize - 1, 0, 5, 'images/redUnit.png')]
    unitsA_merged = [Unit(1, 0, 0, 0, 5, 'images/blueUnit.png')]
    unitsB_merged = [Unit(1, 0, 0, 0, 5, 'images/redUnit.png')]
    armyA = Army('images/blueArmy.png', 0, 0, unitsA, unitsA_merged, 800, False, 1.5)
    armyB = Army('images/redArmy.png', gridSize - 1, gridSize - 1, unitsB, unitsB_merged, 800, False, 1.5)

    grid = Grid(gridSize, armyA, armyB)
    grid.grid[0][0].occupied_by = 1
    grid.grid[gridSize - 1][gridSize - 1].occupied_by = 2
    # Set background
    screen.fill((128, 128, 128))

    blit(screen, timer, grid, w_width, w_height, armyA, armyB)

    running = True

    time_delay = 100
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
    screen.fill((128, 128, 128), rect=(650, 100, 150, 50))
    screen.fill((128, 128, 128), rect=(650, 130, 150, 50))
    screen.fill((128, 128, 128), rect=(650, 160, 150, 50))
    screen.fill((128, 128, 128), rect=(650, 200, 150, 50))
    screen.fill((128, 128, 128), rect=(650, 230, 150, 80))
    screen.fill((128, 128, 128), rect=(650, 270, 150, 80))
    screen.fill((128, 128, 128), rect=(650, 300, 150, 80))
    screen.fill((128, 128, 128), rect=(650, 330, 150, 80))
    font = pygame.font.SysFont('Garamond', 16)
    timerSurface = font.render("Day: " + str(timer), False, (255, 0, 0))
    armyA_Surface = font.render("Gold army A: " + str(armyA.money), False, (212, 175, 55))
    armyB_Surface = font.render("Gold army B: " + str(armyB.money), False, (212, 175, 55))
    armyA_Size = font.render("army A size: " + str(len(armyA.units_merged)), False, (0, 255, 0))
    armyB_Size = font.render("army B size: " + str(len(armyB.units_merged)), False, (0, 255, 0))
    armyA_Morale = font.render("army A morale: " + str(round(armyA.morale, 2)), False, (0, 0, 255))
    armyB_Morale = font.render("army B morale: " + str(round(armyB.morale, 2)), False, (0, 0, 255))
    battle = font.render("BATTLE!!!!", False, (255, 0, 0))
    screen.blit(timerSurface, (650, 100))
    screen.blit(armyA_Surface, (650, 130))
    screen.blit(armyB_Surface, (650, 160))
    screen.blit(armyA_Size, (650, 200))
    screen.blit(armyB_Size, (650, 230))
    if armyA.in_battle:
        screen.blit(armyA_Morale, (650, 270))
        screen.blit(armyB_Morale, (650, 300))
        screen.blit(battle, (650, 330))
