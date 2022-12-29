import dataclasses
import numpy as np
import random
import typing

from evo_sim.algs.repr import Individual


@dataclasses.dataclass
class BinaryPhenotype:
    genotype: str
    length: int = dataclasses.field(init=False)

    def __post_init__(self):
        try:
            int(self.genotype, 2)
        except ValueError as e:
            print(f"Error while creating phenotype: {e}")
            raise e

        self.genotype = self.genotype.replace('0b', '')
        self.length = len(self.genotype)

    def __int__(self) -> int:
        return int(self.genotype, 2)

    def __str__(self) -> str:
        return str(int(self))

    def __repr__(self) -> str:
        return f"BinaryPhenotype(genotype={self.genotype})"

    def __lt__(self, other) -> bool:
        if not isinstance(other, type(self)):
            raise ValueError(f"__lt__ not supported for type {type(other)}")

        return int(self) < int(other)

    def to_individual(self, y_pos: float) -> Individual:
        return Individual(x_pos=float(str(self)), y_pos=y_pos)

    def flip_bit(self, index: int | None = None) -> None:
        if index is None:
            index = random.randint(0, self.length - 1)

        bit = self.genotype[index]
        flipped = bin(int(bit, 2) ^ 1).replace('0b', '')
        self.genotype = \
            self.genotype[:index] + flipped + self.genotype[index + 1:]

    def __add__(self, other) -> tuple['BinaryPhenotype', 'BinaryPhenotype']:
        if not isinstance(other, type(self)):
            raise ValueError(f"__add__ not supported for type {type(other)}")

        assert self.length == other.length, (
            f"Lenght of genotypes mismatch! Self: {self.length}, "
            f"other: {other.length}"
        )

        cut_off = self.length // 2

        new_genotype_1 = self.genotype[:cut_off] + other.genotype[cut_off:]
        new_genotype_2 = other.genotype[:cut_off] + self.genotype[cut_off:]

        offspring_1 = type(self)(new_genotype_1)
        offspring_2 = type(self)(new_genotype_2)

        return (offspring_1, offspring_2)

    @classmethod
    def from_int(cls, value: int, length: int | None = None):
        if not isinstance(value, int):
            raise ValueError(
                f"'from_int' method not supported for type {type(value)}"
            )

        if length is None:
            return cls(bin(value))

        return cls("{0:0{length}b}".format(value, length=length))


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
