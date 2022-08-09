from typing import cast

from overrides import overrides

from src.events.event import Event, ClickEvent, LogicEvent, GraphicEvent
from src.events.event_emitter import EventEmitter
from src.events.event_manager.event_manager import EventManager
from src.events.event_type import ClickEventType, LogicEventType, GraphicEventType
from src.graphics.gui import GUI
from src.object.object_kind import ObjectKind
from src.position import Position


class ClickingEventManager(EventManager):
    def __init__(self, gui: GUI):
        self._events: list[ClickEvent] = []

        self._gui = gui
        self.event_emitter = EventEmitter()

    def _is_clicked_on_pond(self, x, y):
        return 0 <= x < self._gui.settings.screen_pond_width and 0 <= y < self._gui.settings.screen_pond_height

    @overrides
    def add_event(self, event: Event) -> None:
        event = cast(ClickEvent, event)
        self._events.append(event)

    def _handle_add_event(self, event: ClickEvent) -> None:
        if not self._is_clicked_on_pond(event.pos[0], event.pos[1]):
            return

        dummy = self._gui.user_panel.get_dummy()
        click_coor = self._gui.get_click_coor(event.pos)

        if dummy.kind == ObjectKind.ALGA_MAKER and click_coor[1] != self._gui.settings.pond_height - 1:
            return

        self.event_emitter.emit_event(
            LogicEvent(LogicEventType.ADD, dummy, Position(click_coor[1], click_coor[0]))
        )

        self.event_emitter.emit_event(
            GraphicEvent(
                GraphicEventType.ANIM_NEW, pond_object=dummy,
                x=click_coor[0], y=click_coor[1]
            )
        )

    def _handle_check_event(self, event: ClickEvent) -> None:
        pass

    @overrides
    def handle_events(self) -> None:
        cp_events = self._events.copy()
        self._events.clear()

        for event in cp_events:
            if event.event_type == ClickEventType.LEFT_CLICK:
                self._handle_add_event(event)
            elif event.event_type == ClickEventType.RIGHT_CLICK:
                self._handle_check_event(event)

    @overrides
    def clear(self) -> None:
        self._events.clear()
