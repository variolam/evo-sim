import pytest
import random

from evo_sim.algs.evo import BinaryPhenotype


@pytest.fixture
def start_value():
    return '000111'


def test_init(start_value):
    phen = BinaryPhenotype(f'0b{start_value}')
    assert start_value == phen.genotype


def test_str(start_value):
    phen = BinaryPhenotype(start_value)
    assert '7' == str(phen)


def test_int(start_value):
    phen = BinaryPhenotype(start_value)
    assert 7 == int(phen)


def test_mutation(start_value):
    phen = BinaryPhenotype(start_value)
    phen.flip_bit(1)
    assert '010111' == phen.genotype
    assert 23 == int(phen)


def test_crossover():
    phen_1 = BinaryPhenotype('000111')
    phen_2 = BinaryPhenotype('111000')

    off_1, off_2 = phen_1 + phen_2
    off_3, off_4 = phen_2 + phen_1

    assert off_1 is not off_2
    assert off_3 is not off_4
    assert '000000' == off_1.genotype
    assert '111111' == off_2.genotype
    assert '111111' == off_3.genotype
    assert '000000' == off_4.genotype


def test_crossover_odd_length():
    phen_1 = BinaryPhenotype('0001110')
    phen_2 = BinaryPhenotype('1110001')

    off_1, off_2 = phen_1 + phen_2

    assert '0000001' == off_1.genotype
    assert '1111110' == off_2.genotype


def test_crossover_invalid(start_value):
    phen_1 = BinaryPhenotype(start_value)

    with pytest.raises(ValueError):
        phen_1 + 'invalid type'


def test_sorting():
    phen_1 = BinaryPhenotype('000001')
    phen_2 = BinaryPhenotype('001001')
    phen_3 = BinaryPhenotype('100000')

    phen_list = [phen_1, phen_2, phen_3]
    random.shuffle(phen_list)

    phen_list.sort()

    assert phen_1 is phen_list[0]
    assert phen_2 is phen_list[1]
    assert phen_3 is phen_list[2]


def test_init_from_int_none_length():
    phen_1 = BinaryPhenotype.from_int(15)

    assert '1111' == phen_1.genotype


def test_init_from_int_var_length():
    phen_1 = BinaryPhenotype.from_int(15, length=10)

    assert '0000001111' == phen_1.genotype
