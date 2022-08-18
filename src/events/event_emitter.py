from __future__ import annotations

from typing import TYPE_CHECKING, Sequence

import pygame
from pygame.locals import (  # type: ignore
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_MINUS,
    K_EQUALS,
    K_c,
    K_e,
    K_j,
    K_q,
    K_COMMA,
    K_PERIOD,
    QUIT,
    MOUSEBUTTONDOWN,
)

from src.constants import LEFT_MOUSE_BUTTON
from src.decision.decision import Decision
from src.events.event import Event, GameEvent, LogicEvent, GraphicEvent, ClickEvent
from src.events.event_manager.game_event_manager import GameEventManager
from src.events.event_manager.graphic_event_manager import GraphicEventManager
from src.events.event_manager.logic_event_manager import LogicEventManager
from src.events.event_manager.clicking_event_manager import ClickingEventManager
from src.events.event_type import GameEventType, GraphicEventType, ClickEventType
from src.position import Position
from src.singleton import Singleton

if TYPE_CHECKING:
    from src.game import Game


class EventEmitter(metaclass=Singleton):
    def __init__(self):
        self._game_event_manager: GameEventManager = None
        self._graphic_event_manager: GraphicEventManager = None
        self._logic_event_manager: LogicEventManager = None
        self._clicking_event_manager: ClickingEventManager = None

    def setup(self, game: Game) -> None:
        self._game_event_manager = GameEventManager(game)
        self._graphic_event_manager = GraphicEventManager(game.gui, self)
        self._logic_event_manager = LogicEventManager(game.engine)
        self._clicking_event_manager = ClickingEventManager(game.gui, self)

    def emit_events(self, events: list[Event]) -> None:
        for event in events:
            self.emit_event(event)

    def emit_event(self, event: Event) -> None:
        if isinstance(event, GameEvent):
            self._game_event_manager.add_event(event)
        elif isinstance(event, GraphicEvent):
            self._graphic_event_manager.add_event(event)
        elif isinstance(event, LogicEvent):
            self._logic_event_manager.add_event(event)
        elif isinstance(event, ClickEvent):
            self._clicking_event_manager.add_event(event)
        else:
            raise Exception('Unknown type')

    def handle_events(self) -> None:
        self._emit_pygame_events()
        self._game_event_manager.handle_events()
        self._graphic_event_manager.handle_events()
        self._clicking_event_manager.handle_events()
        self._logic_event_manager.handle_events()

    def is_animation_event_present(self) -> bool:
        return self._graphic_event_manager.is_animation_event_present()

    def clear_gui_events(self) -> None:
        self._graphic_event_manager.clear()
        self._clicking_event_manager.clear()

    def emit_anim_move_event(self, decision: Decision, n_pos: Position) -> None:
        self.emit_event(
            GraphicEvent(
                GraphicEventType.ANIM_MOVE, pond_object=decision.pond_object,
                from_x=decision.pond_object.position.x, from_y=decision.pond_object.position.y,
                to_x=n_pos.x, to_y=n_pos.y
            )
        )

    def emit_anim_stay_event(self, decision: Decision) -> None:
        x, y = decision.pond_object.position.x, decision.pond_object.position.y
        self.emit_event(GraphicEvent(GraphicEventType.ANIM_STAY, pond_object=decision.pond_object, x=x, y=y))

    def _emit_pygame_events(self) -> None:
        self._emit_pygame_non_key_events(pygame.event.get())
        self._emit_pygame_key_events(pygame.key.get_pressed())

    def _emit_pygame_non_key_events(self, event_list: list[pygame.event.Event]) -> None:
        for event in event_list:
            if event.type == QUIT:
                self.emit_event(GameEvent(GameEventType.QUIT))
            elif event.type == MOUSEBUTTONDOWN:
                self._emit_clicking_event(event)
            elif event.type == pygame.KEYDOWN:
                if event.key == K_q:
                    self.emit_event(GraphicEvent(GraphicEventType.KEY_PRESSED, key="q"))

    def _emit_pygame_key_events(self, keys: Sequence[bool]) -> None:
        supported_keys = [K_UP, K_DOWN, K_LEFT, K_RIGHT, K_EQUALS, K_MINUS, K_c, K_COMMA, K_PERIOD]
        transformed_keys = ['up', 'down', 'left', 'right', '=', '-', 'c', ',', '.']

        for idx, supported_key in enumerate(supported_keys):
            if keys[supported_key]:
                self.emit_event(GraphicEvent(GraphicEventType.KEY_PRESSED, key=transformed_keys[idx]))

        self._emit_pygame_key_game_events(keys)

    def _emit_pygame_key_game_events(self, keys: Sequence[bool]) -> None:
        if keys[K_e]:
            self.emit_event(GameEvent(GameEventType.QUIT))
        if keys[K_j]:
            self.emit_event(GameEvent(GameEventType.SKIP))

    def _emit_clicking_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == LEFT_MOUSE_BUTTON:
                self.emit_event(ClickEvent(ClickEventType.LEFT_CLICK, pygame.mouse.get_pos()))
