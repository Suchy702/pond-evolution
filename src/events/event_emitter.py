from __future__ import annotations

from typing import Optional, TYPE_CHECKING

import pygame
from pygame.locals import (  # type: ignore
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_MINUS,
    K_EQUALS,
    K_c,
    K_q,
    K_COMMA,
    K_PERIOD,
    QUIT,
    MOUSEBUTTONDOWN,
)

from src.events.event import Event, GameEvent, LogicEvent, GraphicEvent, ClickEvent

if TYPE_CHECKING:
    from src.events.event_manager.game_event_manager import GameEventManager
    from src.events.event_manager.graphic_event_manager import GraphicEventManager
    from src.events.event_manager.logic_event_manager import LogicEventManager
    from src.events.event_manager.clicking_event_manager import ClickingEventManager
from src.events.event_type import GameEventType, GraphicEventType, ClickEventType
from src.singleton import Singleton

LEFT_MOUSE_BUTTON = 1


class EventEmitter(metaclass=Singleton):
    def __init__(self):
        self.game_event_manager: Optional[GameEventManager] = None
        self.graphic_event_manager: Optional[GraphicEventManager] = None
        self.logic_event_manager: Optional[LogicEventManager] = None
        self.clicking_event_manager: Optional[ClickingEventManager] = None

    def emit_event(self, event: Event) -> None:
        if isinstance(event, GameEvent):
            self.game_event_manager.add_event(event)
        elif isinstance(event, GraphicEvent):
            self.graphic_event_manager.add_event(event)
        elif isinstance(event, LogicEvent):
            self.logic_event_manager.add_event(event)
        elif isinstance(event, ClickEvent):
            self.clicking_event_manager.add_event(event)
        else:
            raise Exception('Unknown type')

    def emit_events(self, events: list[Event]) -> None:
        for event in events:
            self.emit_event(event)

    def _emit_pygame_events(self) -> None:
        self._handle_not_pressed_events(pygame.event.get())
        self._emit_pygame_pressed_keys_events(pygame.key.get_pressed())

    def _emit_clicking_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == LEFT_MOUSE_BUTTON:
                self.emit_event(ClickEvent(ClickEventType.LEFT_CLICK, pygame.mouse.get_pos()))
            else:
                self.emit_event(ClickEvent(ClickEventType.RIGHT_CLICK, pygame.mouse.get_pos()))

    def _handle_not_pressed_events(self, event_list):
        for event in event_list:
            if event.type == QUIT:
                self.emit_event(GameEvent(GameEventType.QUIT))
            elif event.type == MOUSEBUTTONDOWN:
                self._emit_clicking_event(event)
            elif event.type == pygame.KEYDOWN:
                if event.key == K_q:
                    self.emit_event(GraphicEvent(GraphicEventType.KEY_PRESSED, key="q"))

    @staticmethod
    def _from_pygame_event(event) -> Event | None:
        if event.type == QUIT:
            return GameEvent(GameEventType.QUIT)
        return None

    def _emit_pygame_pressed_keys_events(self, keys) -> None:
        supported_keys = [K_UP, K_DOWN, K_LEFT, K_RIGHT, K_EQUALS, K_MINUS, K_c, K_COMMA, K_PERIOD]
        transformed_keys = ['up', 'down', 'left', 'right', '=', '-', 'c', ',', '.']

        for idx, supported_key in enumerate(supported_keys):
            if keys[supported_key]:
                self.emit_event(GraphicEvent(GraphicEventType.KEY_PRESSED, key=transformed_keys[idx]))

    def handle_events(self) -> None:
        self._emit_pygame_events()
        self.game_event_manager.handle_events()
        self.graphic_event_manager.handle_events()
        self.logic_event_manager.handle_events()
        self.clicking_event_manager.handle_events()

    def is_animation_event_present(self) -> bool:
        return self.graphic_event_manager.is_animation_event()
