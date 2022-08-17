from __future__ import annotations

import math
from random import randint, random
from typing import Optional, TYPE_CHECKING, cast

from overrides import overrides

from src.ai.ai import AI
from src.decision.decision import Decision
from src.decision.decision_set import DecisionSet
from src.decision.decision_type import DecisionType
from src.object.fish_trait import FishTrait
from src.object.fish_type import FishType
from src.object.object_kind import ObjectKind
from src.object.pond_object import PondObject
from src.pond.pond_viewer import PondViewer
from src.position import Position

from src.constants import (
    CHANCE_TO_SMART_FISH_DO_RANDOM_MOVE,
    CNT_FISH_DIV,
    CHANCE_THAT_FISH_GO_FOR_FOOD,
    CHANCE_THAT_FISH_GO_TO_BOTTOM_FOR_FOOD,
    CHANCE_THAT_FISH_NOT_RUN
)

if TYPE_CHECKING:
    from src.object.fish import Fish


class FishAI(AI["Fish"]):
    def _find_random_pos_to_move(self) -> Position:
        return self.pond_object.pos.changed(
            randint(-self.pond_object.speed, self.pond_object.speed),
            randint(-self.pond_object.speed, self.pond_object.speed)
        )

    def _movement_decision(self, pond_viewer: PondViewer) -> Decision:
        if FishTrait.SMART in self.pond_object.traits:
            return self._smart_movement_decision(pond_viewer)
        return self._random_movement_decision()

    def _emit_move_decision(self, to_x: int, to_y: int) -> Decision:
        return Decision(DecisionType.MOVE, pond_object=self.pond_object, to_x=to_x, to_y=to_y)

    @staticmethod
    def _is_smart_fish_do_random_move() -> bool:
        return random() < CHANCE_TO_SMART_FISH_DO_RANDOM_MOVE

    def _get_fish_layers(self, pond_viewer: PondViewer) -> list[list[Fish]]:
        pos, eyesight = self.pond_object.pos, self.pond_object.eyesight
        fish_layers = list(pond_viewer.get_visible_objects_by_type(pos, eyesight, [ObjectKind.FISH]))
        fish_layers = cast(list[list["Fish"]], fish_layers)
        return fish_layers

    def _define_predator_move_decision(self, fish_layers: list[list[Fish]]) -> Decision:
        decision = self._try_eat_other_fish(fish_layers)
        return self._random_movement_decision() if decision is None else decision

    def _define_non_predator_move_decision(
            self, fish_layers: list[list[Fish]], cnt_fish: int, pond_viewer: PondViewer
    ) -> Decision:
        decision = self._run_away_if_predator_close(fish_layers, cnt_fish)
        if decision is None:
            decision = self._try_eat_other_non_fish(pond_viewer, cnt_fish)

        return self._random_movement_decision() if decision is None else decision

    def _smart_movement_decision(self, pond_viewer: PondViewer) -> Decision:
        if self._is_smart_fish_do_random_move():
            return self._random_movement_decision()

        fish_layers = self._get_fish_layers(pond_viewer)
        cnt_fish = sum([len(layer) for layer in fish_layers])

        if FishTrait.PREDATOR in self.pond_object.traits:
            return self._define_predator_move_decision(fish_layers)

        return self._define_non_predator_move_decision(fish_layers, cnt_fish, pond_viewer)

    def _is_fish_danger_predator(self, fish: Fish) -> bool:
        return FishTrait.PREDATOR in fish.traits and fish.size > self.pond_object.size

    def _find_danger_predator(self, fish_layers: list[list[Fish]]) -> Optional[Fish]:
        for fish_layer in fish_layers[1:-1]:  # skip predators that are in the same cell as current fish
            for fish in fish_layer:
                if self._is_fish_danger_predator(fish):
                    return fish
        return None

    @staticmethod
    def _fish_choose_not_to_run(predator: Fish, cnt_fish: int) -> bool:
        return predator is None or random() < CHANCE_THAT_FISH_NOT_RUN + cnt_fish / CNT_FISH_DIV

    def _calc_diff_x_run(self, predator: Fish) -> int:
        max_diff_dist = min(abs(self.pond_object.pos.x - predator.pos.x), self.pond_object.speed)
        return int(max_diff_dist * math.copysign(1, self.pond_object.pos.x - predator.pos.x))

    def _calc_diff_y_run(self, predator: Fish) -> int:
        max_diff_dist = min(abs(self.pond_object.pos.y - predator.pos.y), self.pond_object.speed)
        return int(max_diff_dist * math.copysign(1, self.pond_object.pos.y - predator.pos.y))

    def _run_away_if_predator_close(self, fish_layers: list[list[Fish]], cnt_fish: int) -> Optional[Decision]:
        predator = self._find_danger_predator(fish_layers)

        if self._fish_choose_not_to_run(predator, cnt_fish):
            return None

        diff_x = self._calc_diff_x_run(predator)
        diff_y = self._calc_diff_y_run(predator)

        return self._emit_move_decision(self.pond_object.pos.x + diff_x, self.pond_object.pos.y + diff_y)

    def _can_eat_other_fish(self, fish: Fish) -> bool:
        return fish.size < self.pond_object.size and FishTrait.PREDATOR not in fish.traits

    def _try_eat_other_fish(self, fish_layers: list[list[Fish]]) -> Optional[Decision]:
        for fish_layer in fish_layers:
            for fish in fish_layer:
                if not self.pond_object.is_position_reachable(fish.pos):
                    break
                if self._can_eat_other_fish(fish):
                    return self._emit_move_decision(fish.pos.x, fish.pos.y)
        return None

    @staticmethod
    def _can_eat_other_non_fish(food: PondObject, pond_viewer: PondViewer, cnt_fish: int) -> bool:
        if food.pos.y == pond_viewer.pond_height - 1:
            return random() < CHANCE_THAT_FISH_GO_TO_BOTTOM_FOR_FOOD - cnt_fish / CNT_FISH_DIV
        return random() < CHANCE_THAT_FISH_GO_FOR_FOOD - cnt_fish / CNT_FISH_DIV

    def _try_eat_other_non_fish(self, pond_viewer: PondViewer, cnt_fish: int) -> Optional[Decision]:
        pos, eyesight = self.pond_object.pos, self.pond_object.eyesight
        food_layers = pond_viewer.get_visible_objects_by_type(pos, eyesight, FishType.get_edible_food(self.pond_object))

        for food_layer in food_layers:
            for food in food_layer:
                if not self.pond_object.is_position_reachable(food.pos):
                    break
                if self._can_eat_other_non_fish(food, pond_viewer, cnt_fish):
                    return self._emit_move_decision(food.pos.x, food.pos.y)

        return None

    def _random_movement_decision(self) -> Decision:
        pos_to_move = self._find_random_pos_to_move()
        return self._emit_move_decision(pos_to_move.x, pos_to_move.y)

    def _reproduce_decision(self) -> Optional[Decision]:
        if self.pond_object.vitality > self.pond_object.vitality_need_to_breed:
            return Decision(DecisionType.REPRODUCE, pond_object=self.pond_object)
        return None

    @overrides
    def get_decisions(self, pond_viewer: PondViewer) -> DecisionSet:
        decisions = DecisionSet()
        reproduce_decision = self._reproduce_decision()
        decisions.add(reproduce_decision)

        if reproduce_decision is None:
            decisions.add(self._movement_decision(pond_viewer))
        else:
            decisions.add(Decision(DecisionType.STAY, pond_object=self.pond_object))

        return decisions
