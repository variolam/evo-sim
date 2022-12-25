import numpy as np

from evo_sim.algs.repr import Individual


class GeneticAlgorithm:

    def __init__(
        self,
        population_size: int,
        max_x: int = 100,
        max_y: int = 100,
    ) -> None:
        self.population_size = population_size
        self._generation = 0
        self.population = [
            Individual(
                x_pos=np.random.uniform(0, high=max_x),
                y_pos=np.random.uniform(0, high=max_y),
            ) for _ in range(population_size)
        ]

    def __call__(self, *args, **kwds) -> list[Individual]:
        return self.population
