import numpy as np
import pygame
from pygame import locals as py_locals
import sys

from evo_sim import algs, exceptions, functions, ui_parts

pygame.init()

# Colours
BACKGROUND_C = (144, 238, 144)
LINE_C = (74, 87, 51)

# Game Setup
FPS = 60
fpsClock = pygame.time.Clock()
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
STARTED = 'False'

WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('evo-sim')


def quit_game():
    pygame.quit()
    sys.exit()


def refresh():
    # Super hacky, but works
    raise exceptions.ResetException()


def draw_triangle(x_pos, y_pos, color=(255, 0, 0), radius=20, offsets=(0, 0)):
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


def start(mode):
    global STARTED
    assert mode in ['False', 'evo', 'bee'], "Mode not recoginzed!"
    STARTED = mode


def start_button_callback():
    start('evo')


def draw_population(population: list[algs.Individual]):
    for idv in population:
        pygame.draw.circle(
            WINDOW,
            color=idv.colour,  # type: ignore
            center=(idv.x_pos, idv.y_pos),
            radius=idv.radius,
        )


# The main function that controls the game
def main():
    first_loop = True
    looping = True
    hill_x = np.arange(WINDOW_WIDTH)
    hill_y = functions.hill(
        len(hill_x),
        scale=WINDOW_HEIGHT / 2.0,
        pos_y=WINDOW_HEIGHT / 4.0
    )

    def fitness_function(x):
        try:
            return hill_y[x]
        except IndexError:
            return hill_y[-1]

    points = list(zip(hill_x, hill_y))
    print(f"Max Point: {max(hill_y)}")
    print(f"Min Point: {min(hill_y)}")

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
    start_button = ui_parts.Button(
        WINDOW,
        'Start Sim',
        (
            WINDOW_WIDTH - refresh_button.size[0] - quit_button.size[0] - 120,
            WINDOW_HEIGHT - 50
        ),
        callback=start_button_callback,
    )

    # Rendered from top down, therefore visually max is our min
    min_index = np.argmin(hill_y)

    gen_algo = algs.GeneticAlgorithm(
        20,
        fitness_function=fitness_function,
        max_x=WINDOW_WIDTH,
    )

    # The main game loop
    while looping:
        WINDOW.fill(BACKGROUND_C)
        pygame.draw.lines(WINDOW, LINE_C, False, points, 3)
        refresh_button.show()
        quit_button.show()
        start_button.show()
        draw_triangle(
            x_pos=hill_x[min_index],
            y_pos=hill_y[min_index],
            radius=8,
            offsets=(0, -50)
        )

        # Get inputs
        for event in pygame.event.get():
            if event.type == py_locals.QUIT:
                quit_game()
            refresh_button.click(event)
            quit_button.click(event)
            start_button.click(event)

        if first_loop:
            population = gen_algo()
            draw_population(population)
            first_loop = False

        if STARTED == 'evo':
            if gen_algo._generation < 500:
                population = gen_algo()
            draw_population(population)

            best_x = int(gen_algo.best_solution)
            best_y = fitness_function(best_x)
            draw_triangle(
                x_pos=best_x,
                y_pos=best_y,
                color=(0, 0, 255),
                offsets=(0, -100)
            )

        # Render elements of the game
        pygame.display.update()
        fpsClock.tick(FPS)


if __name__ == '__main__':
    while True:
        try:
            main()
        except exceptions.ResetException:
            print("Resetting environment...")
