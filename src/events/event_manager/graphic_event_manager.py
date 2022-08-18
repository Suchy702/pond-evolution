from __future__ import annotations

import time
from typing import cast, TYPE_CHECKING

import pygame
from overrides import overrides

from src.constants import SCREEN_MOVE_CHANGE, SCREEN_ZOOM_CHANGE, ANIMATION_SPEED_CHANGE
from src.events.event import GraphicEvent, Event
from src.events.event_manager.event_manager import EventManager
from src.events.event_type import GraphicEventType

if TYPE_CHECKING:
    from src.graphics.gui import GUI
    from src.events.event_emitter import EventEmitter


class GraphicEventManager(EventManager):
    def __init__(self, gui: GUI, event_emitter: EventEmitter):
        self._events: list[GraphicEvent] = []
        self._animation_events: list[GraphicEvent] = []
        self._gui: GUI = gui
        self._event_emitter = event_emitter

        # Needed for fluent speed changing.
        self._animation_speed_changed = False
        self._last_animation_speed_change_time = time.time()

        self._max_anim_step = -1

    @overrides
    def add_event(self, event: Event) -> None:
        event = cast(GraphicEvent, event)
        if event.event_type.name.startswith("ANIM_"):
            self._animation_events.append(event)
        else:
            self._events.append(event)

    def handle_events(self) -> None:
        self._handle_static_events()
        self._handle_animation_events()
        self._animation_speed_changed = False
        self._gui.user_panel.draw()
        pygame.display.update()

    def is_animation_event_present(self) -> bool:
        return len(self._animation_events) > 0

    @overrides
    def clear(self) -> None:
        self._animation_events.clear()
        self._events.clear()

    def _handle_static_events(self) -> None:
        static_events_copy = self._events.copy()
        self._events.clear()

        for event in static_events_copy:
            self._handle_static_event(event)

    def _handle_animation_events(self) -> None:
        anim_events_copy = self._animation_events.copy()
        self._animation_events.clear()

        if len(anim_events_copy) == 0:
            return

        self._set_max_animation_step(anim_events_copy)

        if self._is_only_new_object_which_shouldnt_be_shown(anim_events_copy):
            return

        self._draw_animations_events(anim_events_copy)

    def _handle_static_event(self, event: GraphicEvent) -> None:
        match event.key:
            case "up":
                self._gui.value_guard.y_offset += SCREEN_MOVE_CHANGE
            case "down":
                self._gui.value_guard.y_offset -= SCREEN_MOVE_CHANGE
            case "left":
                self._gui.value_guard.x_offset += SCREEN_MOVE_CHANGE
            case "right":
                self._gui.value_guard.x_offset -= SCREEN_MOVE_CHANGE
            case "=":
                self._gui.zoom(SCREEN_ZOOM_CHANGE)
            case "-":
                self._gui.zoom(-SCREEN_ZOOM_CHANGE)
            case "c":
                self._gui.center_view()
            case ",":
                self._change_animation_speed(ANIMATION_SPEED_CHANGE)
            case ".":
                self._change_animation_speed(-ANIMATION_SPEED_CHANGE)
            case "q":
                self._gui.user_panel.next_object()

    def _handle_animation_event(self, event: GraphicEvent):
        self._set_event_total_step(event)

        if self._animation_speed_changed:
            self._adjust_total_steps(event)

        self._gui.draw_animation_event(event)
        self._add_event_with_next_step(event)

    @staticmethod
    def _is_only_new_object_which_shouldnt_be_shown(events: list[GraphicEvent]) -> bool:
        return len([event for event in events if event.event_type != GraphicEventType.ANIM_NEW]) == 0

    def _set_max_animation_step(self, cp_anim_events: list[GraphicEvent]) -> None:
        self._max_anim_step = -1
        self._max_anim_step = max([event.step for event in cp_anim_events])

    def _draw_animations_events(self, cp_anim_events: list[GraphicEvent]) -> None:
        self._gui.draw_empty_frame()
        for event in cp_anim_events:
            self._handle_animation_event(event)
    def _allow_animation_speed_change(self) -> bool:
        return time.time() - self._last_animation_speed_change_time >= 0.1

    def _change_animation_speed(self, value: int) -> None:
        if not self._allow_animation_speed_change():
            return
        else:
            self._last_animation_speed_change_time = time.time()

        self._gui.value_guard.animation_speed += value
        self._animation_speed_changed = True

    def _add_event_with_next_step(self, event: GraphicEvent) -> None:
        if event.should_make_next_step():
            event.step += 1
            self._event_emitter.emit_event(event)

    def _no_need_to_set_rotate_angle(self, event: GraphicEvent) -> bool:
        is_anim_stay = event.event_type == GraphicEventType.ANIM_STAY
        is_anim_new = event.event_type == GraphicEventType.ANIM_NEW
        return (not self._gui.is_event_for_fish(event)) or is_anim_stay or is_anim_new

    def _initialize_rotate_angle(self, event: GraphicEvent) -> None:
        if self._no_need_to_set_rotate_angle(event):
            return None

        event.is_flipped = self._gui.calculator.is_flipped(event)
        event.rotate = self._gui.calculator.get_rotation_angle(event)

    def _set_event_total_step(self, event: GraphicEvent) -> None:
        if event.total_steps is None:
            event.total_steps = self._gui.value_guard.animation_speed
            event.step = self._max_anim_step
            self._initialize_rotate_angle(event)

    def _adjust_total_steps(self, event: GraphicEvent) -> None:
        percentage = event.step / event.total_steps
        event.total_steps = self._gui.value_guard.animation_speed
        event.step = min(int(event.total_steps * percentage), event.total_steps - 1)
