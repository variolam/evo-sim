from evo_sim.algs.repr import Individual


class GeneticAlgorithm:

    def __init__(self, population_size: int) -> None:
        self.population_size = population_size
        self._generation = 0

    def __call__(self, *args, **kwds) -> list[Individual]:
        pass
