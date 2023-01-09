import json
import numpy as np
import pathlib
import pygame
from pygame import locals as py_locals
import sys
import yaml

if sys.version_info < (3, 10):
    raise RuntimeError(
        f"Python version {sys.version_info} not supported! "
        "Please use Python 3.10 or newer."
    )

from evo_sim import algs, exceptions, functions, ui_parts

pygame.init()

# Colours
BACKGROUND_C = (144, 238, 144)
LINE_C = (74, 87, 51)

# Game Setup
FPS = 60
fpsClock = pygame.time.Clock()
WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 600
STARTED = 'False'
PRINTED_BEST = False

WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('evo-sim')


def quit_game():
    pygame.quit()
    sys.exit()


def refresh():
    # Super hacky, but works
    global STARTED, PRINTED_BEST
    STARTED = 'False'
    PRINTED_BEST = False
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


def algorithm_from_config(config: dict, fitness_function, hill_y):
    if config['use-alg'] == 'evo':
        return algs.GeneticAlgorithm(
            config['evo']['population-size'],
            fitness_function=fitness_function,
            max_x=WINDOW_WIDTH,
            init_x=int(np.argmax(hill_y)),
            mutation_rate=config['evo']['mutation-rate']
        )
    elif config['use-alg'] == 'abc':
        return algs.ABCAlgo(
            config['abc']['population-size'],
            fitness_function=fitness_function,
            max_x=WINDOW_WIDTH,
            init_x=int(np.argmax(hill_y)),
        )
    else:
        raise RuntimeError(f"Algorithm '{config['use-algo']}' not defined!")


def load_config(path: str | pathlib.Path) -> dict:
    path = pathlib.Path(path)
    assert path.exists(), f"Config path {path.absolute()} does not exist!"
    assert path.suffix == '.yaml', 'Only .yaml files are supported for config!'

    with open(path, 'r') as f:
        return yaml.safe_load(f)


# The main function that controls the game
def main():
    global PRINTED_BEST

    config = load_config(pathlib.Path(__file__).parent.parent / 'settings.yaml')  # noqa: E501
    algorithm_used = config['use-alg']
    stop_after = config['stop-after']

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

    algo = algorithm_from_config(config, fitness_function, hill_y)

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
            population = algo.original_population
            draw_population(population)
            first_loop = False

        if STARTED == algorithm_used:
            if algo._generation < stop_after:
                population = algo()
            elif algo._generation >= stop_after and not PRINTED_BEST:
                print(f"Best solution found: {repr(algo.best_solution)}")
                print(f"Global best solution: {np.min(hill_y)}, {np.min(hill_x)}")  # noqa: E501
                print("Logs: ")
                print(json.dumps(algo.log, indent=2))
                PRINTED_BEST = True
            draw_population(population)

        best_x = int(algo.best_solution)
        best_y = algo.best_solution.fitness_val
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
