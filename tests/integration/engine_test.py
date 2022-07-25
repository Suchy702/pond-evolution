from unittest.mock import patch

import pytest

from src.events.event_emitter import EventEmitter
from src.logic.engine import Engine
# noinspection PyUnresolvedReferences
from tests.helper import settings


@pytest.fixture
def engine(settings):
    return Engine(settings)


@patch.object(EventEmitter, 'emit_event')
def test_cycle(engine):
    engine._interactor.preparations()
    for _ in range(5):
        engine.cycle()
        engine.show_pond()
    assert True
