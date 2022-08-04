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
from src.pond.pond_viewer import PondViewer
from src.position import Position

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

    # TODO: później jak zaimplementujemy UI do dodawania rybek to trzeba będzie to całe AI przetestować, bo teraz
    #   nie mam pojęcia czy działa tak jak należy
    def _smart_movement_decision(self, pond_viewer: PondViewer) -> Decision:
        if random() < 0.05:
            return self._random_movement_decision()

        cnt_fish = 0
        fish_layers = list(
            pond_viewer.get_visible_object_by_type(self.pond_object.pos, self.pond_object.eyesight, [ObjectKind.FISH])
        )
        fish_layers = cast(list[list["Fish"]], fish_layers)

        for layer in fish_layers:
            cnt_fish += len(layer)

        if FishTrait.PREDATOR in self.pond_object.traits:
            decision = self._try_eat_other_fish(fish_layers)
            if decision is not None:
                return decision

        if FishTrait.PREDATOR not in self.pond_object.traits:
            decision = self._run_away_if_predator_close(fish_layers)
            if decision is not None:
                return decision

        decision = self._try_eat_other_non_fish(pond_viewer, cnt_fish)
        if decision is not None:
            return decision

        return self._random_movement_decision()

    def _run_away_if_predator_close(self, fish_layers: list[list[Fish]]) -> Optional[Decision]:
        predator = None
        for fish_layer in fish_layers[1:-1]:  # skip predators that are in the same cell as current fish
            for fish in fish_layer:
                if FishTrait.PREDATOR in fish.traits and fish.size > self.pond_object.size:
                    predator = fish
                    break

        if predator is None or random() < 0.1:
            return None

        diff_x = int(min(
            abs(self.pond_object.pos.x - predator.pos.x),
            self.pond_object.speed) * math.copysign(1, self.pond_object.pos.x - predator.pos.x)
                     )

        diff_y = int(min(
            abs(self.pond_object.pos.y - predator.pos.y),
            self.pond_object.speed) * math.copysign(1, self.pond_object.pos.y - predator.pos.y)
                     )

        return Decision(
            DecisionType.MOVE, pond_object=self.pond_object,
            to_x=self.pond_object.pos.x + diff_x, to_y=self.pond_object.pos.y + diff_y
        )

    def _try_eat_other_fish(self, fish_layers: list[list[Fish]]) -> Optional[Decision]:
        for fish_layer in fish_layers:
            for fish in fish_layer:
                if self.pond_object.is_position_reachable(fish.pos):
                    if fish.size < self.pond_object.size and random() < 0.7:
                        return Decision(
                            DecisionType.MOVE, pond_object=self.pond_object, to_x=fish.pos.x, to_y=fish.pos.y
                        )
                else:
                    break
        return None

    def _try_eat_other_non_fish(self, pond_viewer: PondViewer, cnt_fish: int) -> Optional[Decision]:
        for food_layer in pond_viewer.get_visible_object_by_type(
                self.pond_object.pos, self.pond_object.eyesight, FishType.get_edible_food(self.pond_object)
        ):
            for food in food_layer:
                if self.pond_object.is_position_reachable(food.pos):
                    if (food.pos.y < pond_viewer.pond_height - 1 and random() < 0.7 - cnt_fish / 20) or \
                            (food.pos.y == pond_viewer.pond_height - 1 and random() < 0.5 - cnt_fish / 20):
                        return Decision(
                            DecisionType.MOVE, pond_object=self.pond_object, to_x=food.pos.x, to_y=food.pos.y
                        )
                else:
                    break
        return None

    def _random_movement_decision(self) -> Decision:
        pos_to_move = self._find_random_pos_to_move()
        return Decision(DecisionType.MOVE, pond_object=self.pond_object, to_x=pos_to_move.x, to_y=pos_to_move.y)

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
