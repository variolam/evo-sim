import dataclasses
import functools
import numpy as np
import random
import typing

from evo_sim.algs.repr import Individual


@functools.total_ordering
@dataclasses.dataclass(eq=False)
class Foodsource:
    fitness_function: typing.ClassVar[typing.Callable[[int], float]]
    x_loc: float

    def __int__(self) -> int:
        return int(self.x_loc)

    def __str__(self) -> str:
        return str(int(self))

    @property
    def fitness_val(self) -> float:
        return type(self).fitness_function(int(self))

    def __eq__(self, o: 'Foodsource') -> bool:  # type: ignore
        return self.x_loc == o.x_loc

    def __lt__(self, o: 'Foodsource') -> bool:
        return self.x_loc < o.x_loc


class Bee:

    def __init__(
        self,
        _type: typing.Literal['onlooker', 'scout', 'employed'],
        assigned_source: Foodsource | None = None,
    ) -> None:
        self._type = _type
        self._assigned_source = assigned_source


class ABCAlgo:

    def __init__(
        self,
        number_of_solutions: int,
        fitness_function: typing.Callable[[int], float],
        max_x: int = 100,
        init_x: int = 0,
        limit: int = 20,
    ) -> None:
        self.nos = number_of_solutions
        self.fitness_function = fitness_function
        Foodsource.fitness_function = fitness_function
        self.limit = limit
        self._generation = 0
        self.max_x = max_x
        self.best_solution = Foodsource(init_x)
        self.taboo_table: set[int] = set()
        self.log = {  # type: ignore
            'solutions_found_in_gen': {}
        }
        self.food_sources: list[Foodsource] = []
        self.fitness_values: list[float] = []
        self.counters: list[int] = []
        self.probs: list[float] = []
        self.original_population: list[Individual] = []
        self._init_algorithm()

    def _init_algorithm(self) -> None:
        for _ in range(self.nos):
            x_val = random.randint(0, self.max_x)
            f_source = Foodsource(x_val)
            self.food_sources.append(f_source)
            self.counters.append(0)
            self.fitness_values.append(self.fitness_function(x_val))
            self.original_population.append(
                Individual(f_source.x_loc, f_source.fitness_val)
            )

    def __call__(self, *args, **kwds) -> list[Individual]:
        self._generation += 1
        self._employed_phase()
        self._generate_probabilities()
        self._onlooker_phase()

        best_index = np.argmax(self.fitness_values)
        if self.fitness_values[best_index] < self.best_solution.fitness_val:
            self.log['solutions_found_in_gen'][self._generation] = self.food_sources[best_index].fitness_val  # noqa: E501
            self.best_solution = self.food_sources[best_index]

        self._scout_phase()
        return [
            Individual(foodsource.x_loc, foodsource.fitness_val)
            for foodsource in self.food_sources
        ]

    def _scout_phase(self, *args, **kwds):
        for i in range(self.nos):
            if self.counters[i] > self.limit:
                self.taboo_table.add(self.food_sources[i].x_loc)

                while (new_x := random.randint(0, self.max_x)) in self.taboo_table:
                    self.food_sources[i] = Foodsource(new_x)
                    self.counters[i] = 0
                    self.fitness_values[i] = self.fitness_function(self.food_sources[i].fitness_val)  # noqa: E501

    def _employed_phase(self, *args, **kwds):
        for i in range(self.nos):
            neighbor = self.neighborhood(i)

            if (n_fit_val := self.fitness_function(neighbor)) < self.fitness_values[i]:  # noqa: E501
                self.food_sources[i] = Foodsource(neighbor)
                self.fitness_values[i] = n_fit_val
                self.counters[i] = 0
            else:
                self.counters[i] += 1

            # Generate bees to visualize

    def _generate_probabilities(self):
        self.probs = np.array(self.fitness_values) / sum(self.fitness_values)

    def _onlooker_phase(self, *args, **kwds):
        t = 0
        i = 0
        while t < self.nos:
            if random.random() < self.probs[i]:
                t += 1
                neighbor = self.neighborhood(i)

                if (n_fit_val := self.fitness_function(neighbor)) < self.fitness_values[i]:  # noqa: E501
                    self.food_sources[i] = Foodsource(neighbor)
                    self.fitness_values[i] = n_fit_val
                    self.counters[i] = 0
                else:
                    self.counters[i] += 1
            i = (i + 1) % (self.nos - 1)

    def neighborhood(self, solution_index: int) -> int:
        solution = self.food_sources[solution_index].x_loc
        rand_solution_index = solution_index

        while rand_solution_index == solution_index:
            rand_solution_index = random.randint(0, self.nos - 1)

        rand_solution = self.food_sources[rand_solution_index].x_loc
        phi = random.uniform(-1, 1)
        return int(solution + phi * (solution - rand_solution))
