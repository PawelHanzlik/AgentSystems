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

from grid import Grid, drawGrid


def simulation():

    pygame.init()
    # Parameters
    w_width = 600
    w_height = 600
    gridSize = 30

    # Set up the drawing window, adjust the size
    screen = pygame.display.set_mode([w_width, w_height])

    grid = Grid(gridSize)

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
