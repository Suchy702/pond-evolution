import time
from typing import cast

import pygame
from overrides import overrides

from src.constants import SCREEN_MOVE_CHANGE, SCREEN_ZOOM_CHANGE, ANIMATION_SPEED_CHANGE
from src.events.event import GraphicEvent, Event
from src.events.event_emitter import EventEmitter
from src.events.event_manager.event_manager import EventManager
from src.graphics.gui import GUI

event_emitter = EventEmitter()


class GraphicEventManager(EventManager):
    def __init__(self, gui: GUI):
        self._events: list[GraphicEvent] = []
        self._animation_events: list[GraphicEvent] = []
        self._gui: GUI = gui

        # TODO: trzeba zrobić jakiś uniwersalny interfejs jakby było więcej eventów które trzeba wykonywać co x sekund
        # Needed for fluent speed changing
        self._animation_speed_changed = False
        self._last_animation_speed_change_time = time.time()

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

        # TODO: draw_ui chyba nie powinno być tutaj
        self._gui.draw_ui()
        pygame.display.update()

    def handle_events(self) -> None:
        # TODO: To też trzeba ładniej zapisać
        old_speed = self._gui.vals.animation_speed
        self._handle_static_events()
        self._animation_speed_changed = old_speed != self._gui.vals.animation_speed
        self._handle_animation_events()

    def _handle_static_event(self, event: GraphicEvent):
        # TODO: trzeba to jakoś ładniej zapisać
        if event.key in ",." and time.time() - self._last_animation_speed_change_time < 0.1:
            return
        else:
            self._last_animation_speed_change_time = time.time()

        match event.key:
            case "up":
                self._gui.vals.y_offset += SCREEN_MOVE_CHANGE
            case "down":
                self._gui.vals.y_offset -= SCREEN_MOVE_CHANGE
            case "left":
                self._gui.vals.x_offset += SCREEN_MOVE_CHANGE
            case "right":
                self._gui.vals.x_offset -= SCREEN_MOVE_CHANGE
            case "=":
                self._gui.zoom(SCREEN_ZOOM_CHANGE)
            case "-":
                self._gui.zoom(-SCREEN_ZOOM_CHANGE)
            case "c":
                self._gui.center_view()
            case ",":
                self._gui.vals.animation_speed += ANIMATION_SPEED_CHANGE
            case ".":
                self._gui.vals.animation_speed -= ANIMATION_SPEED_CHANGE

    @staticmethod
    def _add_event_with_next_step(event: GraphicEvent) -> None:
        if event.step < event.total_steps:
            n_event = event.copy()
            n_event.step += 1
            event_emitter.emit_event(n_event)

    def _set_event_total_step(self, event: GraphicEvent):
        if event.total_steps is None:
            event.total_steps = self._gui.vals.animation_speed

    def _handle_animation_event(self, event: GraphicEvent):
        self._set_event_total_step(event)

        if self._animation_speed_changed:
            percentage = event.step / event.total_steps
            event.total_steps = self._gui.vals.animation_speed
            event.step = min(int(event.total_steps * percentage), event.total_steps - 1)

        self._gui.draw_anim_event(event)
        self._add_event_with_next_step(event)

    def is_animation_event(self):
        return len(self._animation_events) > 0
