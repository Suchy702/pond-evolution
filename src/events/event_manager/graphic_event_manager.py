import pygame
from overrides import overrides

from src.events.event import GraphicEvent, Event
from src.events.event_emitter import EventEmitter
from src.events.event_manager.event_manager import EventManager
from src.events.event_type import GraphicEventType
from src.graphics.gui import GUI
from src.constants import MOVE_SCREEN_BY_CLICK, ZOOM_SCREEN_BY_CLICK

event_emitter = EventEmitter()


class GraphicEventManager(EventManager):
    def __init__(self, gui: GUI):
        self._events: list[GraphicEvent] = []
        self._animation_events: list[GraphicEvent] = []
        self._gui: GUI = gui

    @overrides
    def add_event(self, event: GraphicEvent) -> None:
        if event.event_type.name.startswith("ANIM_"):
            self._animation_events.append(event)
        else:
            self._events.append(event)

    def handle_events(self) -> None:
        cp_events = self._events.copy()
        cp_anim_events = self._animation_events.copy()

        for event in cp_events:
            self._handle_static_event(event)

        self._gui.draw_empty_frame()
        for event in cp_anim_events:
            self._handle_animation_event(event)
        pygame.display.update()

        # Delete old events. During previous loop some events might have been emitted. We need to make sure not to
        # delete them.
        n_events = []
        cp_events_set = set(cp_events)
        for event in self._events:
            if event not in cp_events_set:
                n_events.append(event)

        n_anim_events = []
        cp_anim_events_set = set(cp_anim_events)
        for event in self._animation_events:
            if event not in cp_anim_events_set:
                n_anim_events.append(event)

        self._events = n_events
        self._animation_events = n_anim_events

    def _handle_static_event(self, event: GraphicEvent):
        if event.event_type == GraphicEventType.KEY_PRESSED:
            match event.key:
                case "up":
                    self._gui.change_y_offset(MOVE_SCREEN_BY_CLICK)
                case "down":
                    self._gui.change_y_offset(-MOVE_SCREEN_BY_CLICK)
                case "left":
                    self._gui.change_x_offset(MOVE_SCREEN_BY_CLICK)
                case "right":
                    self._gui.change_x_offset(-MOVE_SCREEN_BY_CLICK)
                case "=":
                    self._gui.zoom(ZOOM_SCREEN_BY_CLICK)
                case "-":
                    self._gui.zoom(-ZOOM_SCREEN_BY_CLICK)
                case "c":
                    self._gui.center_view()
                case ",":
                    self._gui.settings.animation_speed = min(100, self._gui.settings.animation_speed + 1)
                case ".":
                    self._gui.settings.animation_speed = max(1, self._gui.settings.animation_speed - 1)

    def _handle_animation_event(self, event: GraphicEvent):
        if event.total_steps is None:
            event.total_steps = self._gui.settings.animation_speed

        x, y = None, None

        if event.event_type == GraphicEventType.ANIM_MOVE:
            x1 = event.from_x * self._gui.cell_size + self._gui.x_offset
            y1 = event.from_y * self._gui.cell_size + self._gui.y_offset
            x2 = event.to_x * self._gui.cell_size + self._gui.x_offset
            y2 = event.to_y * self._gui.cell_size + self._gui.y_offset

            if x1 == x2:
                dist = y2 - y1
                y = y1 + dist * event.step / event.total_steps
                x = x1
            else:
                dist = x2 - x1
                a = (y2 - y1) / (x2 - x1)
                b = y1 - a * x1

                x = x1 + dist * event.step / event.total_steps
                y = a * x + b

        elif event.event_type == GraphicEventType.ANIM_STAY:
            x = event.x * self._gui.cell_size + self._gui.x_offset
            y = event.y * self._gui.cell_size + self._gui.y_offset

        if event.step < event.total_steps:
            n_event = event.copy()
            n_event.step += 1
            event_emitter.emit_event(n_event)

        self._gui.draw_object(event.pond_object, x, y)

    def is_animation_event(self):
        return len(self._animation_events) > 0
