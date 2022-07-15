import re

import pytest

from src.events.event import GraphicEvent
from src.events.event_type import GraphicEventType


@pytest.fixture
def graphic_event():
    return GraphicEvent(GraphicEventType.ANIM_MOVE, key='k', x=10, step=1, total_steps=10)


def test_graphic_event_copy(graphic_event):
    cp = graphic_event.copy()
    assert id(cp) != id(graphic_event)
    for attr in GraphicEvent.attributes:
        assert getattr(cp, attr) == getattr(graphic_event, attr)


def test_have_to_make_next_step(graphic_event):
    assert graphic_event.have_to_make_next_step()
    graphic_event.step = 10
    assert not graphic_event.have_to_make_next_step()


def test_graphic_event_str_format(graphic_event):
    assert re.search(r'GraphicEvent\([a-zA-Z_]+\)', str(graphic_event))
