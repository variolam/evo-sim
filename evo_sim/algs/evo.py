import numpy as np
import typing

from evo_sim.algs.repr import Individual


class GeneticAlgorithm:

    def __init__(
        self,
        population_size: int,
        fitness_function: typing.Callable[[int], float],
        max_x: int = 100,
    ) -> None:
        self.population_size = population_size
        self.fitness_function = fitness_function
        self._generation = 0

        self.population = []
        for _ in range(population_size):
            x_pos = np.random.randint(0, high=max_x)
            y_pos = fitness_function(x_pos)
            idv = Individual(x_pos=x_pos, y_pos=y_pos)
            self.population.append(idv)

    def __call__(self, *args, **kwds) -> list[Individual]:
        return self.population
