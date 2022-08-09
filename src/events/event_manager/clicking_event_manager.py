from typing import cast

from overrides import overrides

from src.events.event import Event, ClickEvent, LogicEvent, GraphicEvent
from src.events.event_emitter import EventEmitter
from src.events.event_manager.event_manager import EventManager
from src.events.event_type import ClickEventType, LogicEventType, GraphicEventType
from src.graphics.gui import GUI
from src.object.object_kind import ObjectKind
from src.object.pond_object import PondObject
from src.position import Position


class ClickingEventManager(EventManager):
    def __init__(self, gui: GUI):
        self._events: list[ClickEvent] = []

        self._gui: GUI = gui
        self.event_emitter: EventEmitter = EventEmitter()

    def _is_clicked_on_pond(self, x: int, y: int) -> bool:
        return 0 <= x < self._gui.settings.screen_pond_width and 0 <= y < self._gui.settings.screen_pond_height

    @overrides
    def add_event(self, event: Event) -> None:
        event = cast(ClickEvent, event)
        self._events.append(event)

    def _emit_add_event(self, dummy: PondObject, click_coor: tuple[int, int]) -> None:
        event = LogicEvent(LogicEventType.ADD, dummy, Position(click_coor[1], click_coor[0]))
        self.event_emitter.emit_event(event)

    def _emit_anim_new_event(self, dummy: PondObject, click_coor: tuple[int, int]) -> None:
        event = GraphicEvent(GraphicEventType.ANIM_NEW, pond_object=dummy, x=click_coor[0], y=click_coor[1])
        self.event_emitter.emit_event(event)

    @staticmethod
    def _is_alg(dummy: PondObject) -> bool:
        return dummy.kind == ObjectKind.ALGA_MAKER

    def _is_clicked_on_bottom(self, y: int) -> bool:
        return y != self._gui.settings.pond_height - 1

    def _handle_add_event(self, event: ClickEvent) -> None:
        if not self._is_clicked_on_pond(event.pos[0], event.pos[1]):
            return

        dummy = self._gui.user_panel.get_dummy()
        click_coor = self._gui.get_click_coor(event.pos)

        if self._is_alg(dummy) and self._is_clicked_on_bottom(click_coor[1]):
            return

        self._emit_add_event(dummy, click_coor)
        self._emit_anim_new_event(dummy, click_coor)

    @overrides
    def handle_events(self) -> None:
        cp_events = self._events.copy()
        self._events.clear()

        for event in cp_events:
            if event.event_type == ClickEventType.LEFT_CLICK:
                self._handle_add_event(event)

    @overrides
    def clear(self) -> None:
        self._events.clear()
