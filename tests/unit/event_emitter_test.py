from unittest.mock import Mock

import pytest

from src.events.event import GraphicEvent
from src.events.event_emitter import EventEmitter
from src.events.event_type import GraphicEventType


@pytest.fixture
def event_emitter():
    return EventEmitter()


def test_emit_event(event_emitter):
    event_emitter._graphic_event_manager = Mock()
    graphic_event = GraphicEvent(GraphicEventType.ANIM_MOVE)
    event_emitter.emit_event(graphic_event)
    event_emitter._graphic_event_manager.add_event.assert_called_once()


def test_emit_events(event_emitter):
    event_emitter._graphic_event_manager = Mock()
    graphic_event = GraphicEvent(GraphicEventType.ANIM_MOVE)
    events = [graphic_event.copy() for _ in range(10)]
    event_emitter.emit_events(events)
    assert event_emitter._graphic_event_manager.add_event.call_count == 10
