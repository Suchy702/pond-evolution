import time
from typing import cast

import pygame
from overrides import overrides

from src.constants import SCREEN_MOVE_CHANGE, SCREEN_ZOOM_CHANGE, ANIMATION_SPEED_CHANGE
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

        # Needed for fluent speed changing
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

    def _handle_static_events(self) -> None:
        cp_static_events = self._events.copy()
        self._events.clear()

        for event in cp_static_events:
            self._handle_static_event(event)

    @staticmethod
    def _is_only_new_object_which_shouldnt_be_shown(events: list[GraphicEvent]) -> bool:
        return len([event for event in events if event.event_type != GraphicEventType.ANIM_NEW]) == 0

    def _set_max_anim_step(self, cp_anim_events: list[GraphicEvent]) -> None:
        self._max_anim_step = -1
        self._max_anim_step = max([event.step for event in cp_anim_events])

    def _draw_animations_events(self, cp_anim_events: list[GraphicEvent]) -> None:
        self._gui.draw_empty_frame()
        for event in cp_anim_events:
            self._handle_animation_event(event)

    def _handle_animation_events(self) -> None:
        cp_anim_events = self._animation_events.copy()
        self._animation_events.clear()

        if len(cp_anim_events) == 0:
            return

        self._set_max_anim_step(cp_anim_events)

        if self._is_only_new_object_which_shouldnt_be_shown(cp_anim_events):
            return

        self._draw_animations_events(cp_anim_events)

    def handle_events(self) -> None:
        self._handle_static_events()
        self._handle_animation_events()
        self._animation_speed_changed = False
        self._gui.user_panel.draw()
        pygame.display.update()

    def is_too_small_time_diff_between_anim_changes(self) -> bool:
        return time.time() - self._last_animation_speed_change_time < 0.1

    def change_animation_speed(self, val: int) -> None:
        if self.is_too_small_time_diff_between_anim_changes():
            return
        else:
            self._last_animation_speed_change_time = time.time()
        self._gui.vals.animation_speed += val
        self._animation_speed_changed = True

    def _handle_static_event(self, event: GraphicEvent) -> None:
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
                self.change_animation_speed(ANIMATION_SPEED_CHANGE)
            case ".":
                self.change_animation_speed(-ANIMATION_SPEED_CHANGE)
            case "q":
                self._gui.user_panel.next_add_object()

    @staticmethod
    def _add_event_with_next_step(event: GraphicEvent) -> None:
        if event.have_to_make_next_step():
            event.step += 1
            event_emitter.emit_event(event)

    def _initialize_rotate_angle(self, event: GraphicEvent) -> None:
        if not self._gui.is_obj_fish(event) or event.event_type == GraphicEventType.ANIM_STAY:
            return None

        event.is_flipped = self._gui.calcus.is_flipped(event)
        event.rotate = self._gui.calcus.get_rotate_angle(event)

    def _set_event_total_step(self, event: GraphicEvent) -> None:
        if event.total_steps is None:
            event.total_steps = self._gui.vals.animation_speed
            event.step = self._max_anim_step
            self._initialize_rotate_angle(event)

    def _customize_total_steps_to_anim_speed(self, event: GraphicEvent) -> None:
        percentage = event.step / event.total_steps
        event.total_steps = self._gui.vals.animation_speed
        event.step = min(int(event.total_steps * percentage), event.total_steps - 1)

    def _handle_animation_event(self, event: GraphicEvent):
        self._set_event_total_step(event)

        if self._animation_speed_changed:
            self._customize_total_steps_to_anim_speed(event)

        self._gui.draw_anim_event(event)
        self._add_event_with_next_step(event)

    def is_animation_event(self) -> bool:
        return len(self._animation_events) > 0

    @overrides
    def clear(self) -> None:
        self._events.clear()
        self._animation_events.clear()
