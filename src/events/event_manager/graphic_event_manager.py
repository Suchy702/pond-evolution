from typing import cast

import pygame
from overrides import overrides

from src.constants import MOVE_SCREEN_BY_CLICK, ZOOM_SCREEN_BY_CLICK
from src.events.event import GraphicEvent, Event
from src.events.event_emitter import EventEmitter
from src.events.event_manager.event_manager import EventManager
from src.events.event_type import GraphicEventType
from src.graphics.gui import GUI

event_emitter = EventEmitter()


class GraphicEventManager(EventManager):
    def __init__(self, gui: GUI):
        self._events: list[GraphicEvent] = []
        self._animation_events: list[GraphicEvent] = []
        self._gui: GUI = gui

    @overrides
    def add_event(self, event: Event) -> None:
        event = cast(GraphicEvent, event)
        if event.event_type.name.startswith("ANIM_"):
            self._animation_events.append(event)
        else:
            self._events.append(event)

    def _handle_static_events(self) -> None:
        cp_events = self._events.copy()
        self._events.clear()

        for event in cp_events:
            self._handle_static_event(event)

    def _handle_animation_events(self) -> None:
        cp_anim_events = self._animation_events.copy()
        self._animation_events.clear()

        self._gui.draw_empty_frame()
        for event in cp_anim_events:
            self._handle_animation_event(event)

        pygame.display.update()

    def handle_events(self) -> None:
        self._handle_static_events()
        self._handle_animation_events()

    def _handle_static_event(self, event: GraphicEvent):
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

    def _find_pos_to_draw_when_move(self, event: GraphicEvent) -> tuple[int, int]:
        x1 = event.from_x * self._gui.cell_size + self._gui.x_offset
        y1 = event.from_y * self._gui.cell_size + self._gui.y_offset
        x2 = event.to_x * self._gui.cell_size + self._gui.x_offset
        y2 = event.to_y * self._gui.cell_size + self._gui.y_offset

        if x1 == x2:
            dist = y2 - y1
            y = int(y1 + dist * event.step / event.total_steps)
            x = x1
        else:
            dist = x2 - x1
            a = (y2 - y1) / (x2 - x1)
            b = y1 - a * x1

            x = int(x1 + dist * event.step / event.total_steps)
            y = int(a * x + b)
        return x, y

    def _find_pos_to_draw_when_stay(self, event: GraphicEvent) -> tuple[int, int]:
        x = int(event.x * self._gui.cell_size + self._gui.x_offset)
        y = int(event.y * self._gui.cell_size + self._gui.y_offset)
        return x, y

    def _find_pos_to_draw(self, event: GraphicEvent) -> tuple[int, int]:
        if event.event_type == GraphicEventType.ANIM_MOVE:
            return self._find_pos_to_draw_when_move(event)
        else:
            return self._find_pos_to_draw_when_stay(event)

    @staticmethod
    def _add_event_with_next_step(event: GraphicEvent) -> None:
        if event.step < event.total_steps:
            n_event = event.copy()
            n_event.step += 1
            event_emitter.emit_event(n_event)

    def _set_event_total_step(self, event: GraphicEvent):
        if event.total_steps is None:
            event.total_steps = self._gui.settings.animation_speed

    def _handle_animation_event(self, event: GraphicEvent):
        self._set_event_total_step(event)
        x, y = self._find_pos_to_draw(event)
        self._add_event_with_next_step(event)
        self._gui.draw_object(event.pond_object, x, y)

    def is_animation_event(self):
        return len(self._animation_events) > 0
