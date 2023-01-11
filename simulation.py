import pygame
from pygame.locals import (
    QUIT,
    KEYDOWN,
    K_ESCAPE
)

from army import Army
from grid import Grid, drawGrid
from kingdom import Kingdom
from unit import Unit


def simulation():
    pygame.init()
    timer = 0

    w_width = 900
    w_height = 600
    gridSize = 20

    screen = pygame.display.set_mode([w_width, w_height])
    font = pygame.font.SysFont('arial', 16)

    screen.fill((128, 128, 128))
    unitA = Unit(1, 0, 0, 0, 5, 'images/blueUnit.png')
    unitB = Unit(1, gridSize - 1, gridSize - 1, 0, 5, 'images/redUnit.png')
    unitsA = []
    unitsB = []
    unitsA_merged = [unitA]
    unitsB_merged = [unitB]
    armyA = Army('images/blueArmy.png', 0, 1, 0, 0, unitsA, unitsA_merged, 800, False, 1.5)
    armyB = Army('images/redArmy.png', 0, 2, gridSize - 1, gridSize - 1, unitsB, unitsB_merged, 800, False, 1.5)
    armiesA = [armyA]
    armiesB = [armyB]
    kingdomA = Kingdom(1, armiesA, 8000, 20.0)
    kingdomB = Kingdom(2, armiesB, 8000, 20.0)

    grid = Grid(gridSize, kingdomA, kingdomB)
    grid.grid[0][0].occupied_by = 1
    grid.grid[gridSize - 1][gridSize - 1].occupied_by = 2

    screen.fill((128, 128, 128))

    blit(screen, timer, grid, w_width, w_height, kingdomA, kingdomB)

    running = True

    time_delay = 100
    timer_event = pygame.USEREVENT + 1
    pygame.time.set_timer(timer_event, time_delay)

    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False

            if event.type == timer_event:
                timer += 1
                grid.update()
                blit(screen, timer, grid, w_width, w_height, kingdomA, kingdomB)

        pygame.display.flip()

        if kingdomA.morale <= 0:
            victory_msg = font.render("Kingdom B Victory!", False, (0, 0, 255))
            screen.blit(victory_msg, (650, 420))
            pygame.display.flip()
            gatherFinalInfo(grid)
            while running:
                for event in pygame.event.get():
                    if event.type == QUIT:
                        running = False
                    if event.type == KEYDOWN:
                        if event.key == K_ESCAPE:
                            running = False
        elif kingdomB.morale <= 0:
            victory_msg = font.render("Kingdom A Victory!", False, (0, 0, 255))
            screen.blit(victory_msg, (650, 420))
            pygame.display.flip()
            gatherFinalInfo(grid)
            while running:
                for event in pygame.event.get():
                    if event.type == QUIT:
                        running = False
                    if event.type == KEYDOWN:
                        if event.key == K_ESCAPE:
                            running = False

    pygame.quit()


def blit(screen, timer, grid, w_width, w_height, kingdomA, kingdomB):
    drawGrid(screen, grid, w_width, w_height)
    screen.fill((128, 128, 128), rect=(650, 100, 150, 150))
    screen.fill((128, 128, 128), rect=(650, 130, 250, 250))
    screen.fill((128, 128, 128), rect=(650, 160, 250, 250))
    screen.fill((128, 128, 128), rect=(650, 200, 150, 150))
    screen.fill((128, 128, 128), rect=(650, 230, 150, 180))
    screen.fill((128, 128, 128), rect=(650, 270, 150, 180))
    screen.fill((128, 128, 128), rect=(650, 300, 150, 180))
    screen.fill((128, 128, 128), rect=(650, 330, 150, 180))
    font = pygame.font.SysFont('arial', 16)
    timerSurface = font.render("Day: " + str(timer), False, (255, 0, 0))
    armyA_Surface = font.render("Gold kingdom A: " + str(kingdomA.money), False, (212, 175, 55))
    armyB_Surface = font.render("Gold kingdom B: " + str(kingdomB.money), False, (212, 175, 55))
    a_size = 0
    b_size = 0
    for i in kingdomA.armies:
        a_size += len(i.units) + len(i.units_merged)
    for i in kingdomB.armies:
        b_size += len(i.units) + len(i.units_merged)
    armyA_Size = font.render("kingdom A size: " + str(a_size), False, (0, 255, 0))
    armyB_Size = font.render("kingdom B size: " + str(b_size), False, (0, 255, 0))
    kingdomA_morale = font.render("A morale: " + str(round(kingdomA.morale, 2)), False, (0, 0, 255))
    kingdomB_morale = font.render("B morale: " + str(round(kingdomB.morale, 2)), False, (0, 0, 255))
    screen.blit(timerSurface, (650, 100))
    screen.blit(armyA_Surface, (650, 130))
    screen.blit(armyB_Surface, (650, 160))
    screen.blit(armyA_Size, (650, 200))
    screen.blit(armyB_Size, (650, 230))
    screen.blit(kingdomA_morale, (650, 270))
    screen.blit(kingdomB_morale, (650, 300))
    for a in kingdomA.armies:
        if a.in_battle:
            battle = font.render(f"({a.pos_x}, {a.pos_y}) BATTLE!!!!", False, (255, 0, 0))
            armyA_Morale = font.render("army A morale: " + str(round(a.morale, 2)), False, (0, 0, 255))
            armyB_Morale = font.render("army B morale: " + str(round(a.opponent.morale, 2)), False, (0, 0, 255))
            screen.blit(armyA_Morale, (650, 360))
            screen.blit(armyB_Morale, (650, 390))
            screen.blit(battle, (650, 330))
            break


def gatherFinalInfo(grid):
    occA = 0
    occB = 0
    fields = 0
    for row in grid.grid:
        for field in row:
            fields += 1
            if field.occupied_by == 1:
                occA += 1
            elif field.occupied_by == 2:
                occB += 1
    print(occA, " ", occB, " ", len(grid.grid))
    print(occA/fields, " ", occB/fields)
