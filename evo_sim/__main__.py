import numpy as np
import pygame
from pygame import locals
import sys

from evo_sim import exceptions, functions, ui_parts

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
pygame.display.set_caption('evo-sim')


def quit_game():
    pygame.quit()
    sys.exit()


def refresh():
    # Super hacky, but works
    raise exceptions.ResetException()


def draw_max(x_pos, y_pos, color=(255, 0, 0), radius=20, offsets=(0, 0)):
    x_pos = x_pos + offsets[0]
    y_pos = y_pos + offsets[1]

    pygame.draw.polygon(
        WINDOW,
        color=color,
        points=[
            (x_pos, y_pos),
            (x_pos - 8, y_pos - 8),
            (x_pos + 8, y_pos - 8)
        ]
    )


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
        (WINDOW_WIDTH - 80, WINDOW_HEIGHT - 50),
        callback=refresh,
    )
    quit_button = ui_parts.Button(
        WINDOW,
        'Quit',
        (WINDOW_WIDTH - refresh_button.size[0] - 60, WINDOW_HEIGHT - 50),
        callback=quit_game,
    )
    refresh_button.show()
    quit_button.show()

    # Rendered from top down, therefore visually max is our min
    min_index = np.argmin(hill_y)
    draw_max(
        x_pos=hill_x[min_index],
        y_pos=hill_y[min_index],
        radius=8,
        offsets=(0, -50)
    )

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
    while True:
        try:
            main()
        except exceptions.ResetException:
            print("Resetting environment...")
