import pytest

from evo_sim.algs.evo import BinaryPhenotype


@pytest.fixture
def start_value():
    return '000111'


def test_str(start_value):
    phen = BinaryPhenotype(start_value)
    assert start_value == str(phen)
