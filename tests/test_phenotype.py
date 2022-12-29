import pytest

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
