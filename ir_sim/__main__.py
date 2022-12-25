import numpy as np
import pygame
from pygame import locals
import sys

from ir_sim import functions, ui_parts

pygame.init()

# Colours
BACKGROUND_C = (144, 238, 144)
LINE_C = (74, 87, 51)

# Game Setup
FPS = 60
fpsClock = pygame.time.Clock()
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('IR-Sim')


def quit_game():
    pygame.quit()
    sys.exit()


# The main function that controls the game
def main():
    looping = True
    hill_x = np.arange(WINDOW_WIDTH)
    hill_y = functions.hill(
        len(hill_x),
        scale=WINDOW_HEIGHT / 2.0,
        pos_y=WINDOW_HEIGHT / 4.0
    )

    points = list(zip(hill_x, hill_y))
    print(f"Max Point: {max(hill_y)}")
    print(f"Min Point: {min(hill_y)}")
    WINDOW.fill(BACKGROUND_C)
    pygame.draw.lines(WINDOW, LINE_C, False, points, 3)

    refresh_button = ui_parts.Button(
        WINDOW,
        'Refresh',
        (WINDOW_WIDTH - 80, WINDOW_HEIGHT - 50)
    )
    quit_button = ui_parts.Button(
        WINDOW,
        'Quit',
        (WINDOW_WIDTH - refresh_button.size[0] - 60, WINDOW_HEIGHT - 50),
        callback=quit_game,
    )
    refresh_button.show()
    quit_button.show()

    # The main game loop
    while looping:
        # Get inputs
        for event in pygame.event.get():
            if event.type == locals.QUIT:
                quit_game()
            refresh_button.click(event)
            quit_button.click(event)

        # Processing
        # This section will be built out later

        # Render elements of the game
        pygame.display.update()
        fpsClock.tick(FPS)


if __name__ == '__main__':
    main()
