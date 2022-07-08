import pytest

from src.engine import Engine
from src.simulation_settings import SimulationSettings


@pytest.fixture
def sample_engine():
    return Engine(SimulationSettings(10, 10))


def test_cycle_does_work_properly(sample_engine):
    sample_engine._interactor.preparations()
    for _ in range(5):
        sample_engine.cycle()
        sample_engine.show_pond()
    assert True
