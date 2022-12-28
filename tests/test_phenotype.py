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


def test_flip(start_value):
    phen = BinaryPhenotype(start_value)
    phen.flip_bit(1)
    assert '010111' == phen.genotype
    assert 23 == int(phen)
