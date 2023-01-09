import dataclasses
import functools
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


class ABCAlgo:

    def __init__(
        self,
        number_of_solutions: int,
        fitness_function: typing.Callable[[int], float],
        max_x: int = 100,
        init_x: int = 0,
    ) -> None:
        self.nos = number_of_solutions
        self.fitness_function = fitness_function
        self._generation = 0
        self.max_x = max_x
        self.best_solution = Foodsource(init_x)
        self.log = {  # type: ignore
            'solutions_found_in_gen': {}
        }

    def __call__(self, *args, **kwds) -> list[Individual]:
        ...
