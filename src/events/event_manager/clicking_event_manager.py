from typing import cast

from overrides import overrides

from src.events.event_manager.event_manager import EventManager
from src.events.event import Event, ClickEvent, LogicEvent, GraphicEvent
from src.events.event_type import ClickEventType, LogicEventType, GraphicEventType
from src.graphics.gui import GUI
from src.events.event_emitter import EventEmitter
from src.position import Position


class ClickingEventManager(EventManager):
    def __init__(self, gui: GUI):
        self._add_events = []
        self._check_events = []

        self._gui = gui
        self.event_emitter = EventEmitter()

    def _is_clicked_on_pond(self, x, y):
        return 0 <= x <= self._gui.settings.screen_width and 0 <= y <= self._gui.settings.screen_pond_height

    def _is_adding_event(self, event: ClickEvent):
        return self._is_clicked_on_pond(event.pos[0], event.pos[1]) and event.event_type == ClickEventType.LEFT_CLICK

    @overrides
    def add_event(self, event: Event) -> None:
        event = cast(ClickEvent, event)
        if self._is_adding_event(event):
            self._add_events.append(event)
        else:
            self._check_events.append(event)

    def _handle_add_event(self, event: ClickEvent) -> None:
        adding_obj_str, dummy = self._gui.ui.adding_object
        click_coor = self._gui.get_click_coor(event.pos)
        if adding_obj_str == "alga_maker" and click_coor[1] != self._gui.settings.pond_height-1:
            return

        self.event_emitter.emit_event(
            LogicEvent(LogicEventType.ADD, adding_obj_str, Position(click_coor[1], click_coor[0]))
        )

        self.event_emitter.emit_event(
            GraphicEvent(
                GraphicEventType.ANIM_NEW, pond_object=dummy,
                x=click_coor[0], y=click_coor[1]
            )
        )

    def _handle_add_events(self) -> None:
        cp_events = self._add_events.copy()
        self._add_events.clear()

        for event in cp_events:
            self._handle_add_event(event)

    def _handle_check_event(self, event: ClickEvent) -> None:
        pass

    def _handle_check_events(self) -> None:
        cp_events = self._check_events.copy()
        self._check_events.clear()

        for event in cp_events:
            self._handle_check_event(event)

    @overrides
    def handle_events(self) -> None:
        self._handle_add_events()
        self._handle_check_events()
