from random import randint

from overrides import overrides

from src.ai.ai import AI
from src.decision.decision import Decision
from src.decision.decision_set import DecisionSet
from src.decision.decision_type import DecisionType
from src.object.fish_trait import FishTrait
from src.object.fish_type import FishType
from src.pond_viewer import PondViewer
from src.position import Position


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

    def _smart_movement_decision(self, pond_viewer: PondViewer) -> Decision:
        # TODO: musimy się upewnić że w other_fish nie ma martwych ryb
        if FishTrait.PREDATOR in self.pond_object.traits:
            for fish_layer in pond_viewer.get_visible_object_by_trait(
                    self.pond_object.pos, self.pond_object.eyesight, [FishTrait.PREDATOR], True
            ):
                for fish in fish_layer:
                    if fish.is_alive() and self.pond_object.is_position_reachable(fish.pos):
                        return Decision(
                            DecisionType.MOVE, pond_object=self.pond_object, to_x=fish.pos.x, to_y=fish.pos.y
                        )
                    else:
                        break

        for food_layer in pond_viewer.get_visible_object_by_type(
                self.pond_object.pos, self.pond_object.eyesight, FishType.get_edible_food(self.pond_object)
        ):
            for food in food_layer:
                if self.pond_object.is_position_reachable(food.pos):
                    return Decision(
                        DecisionType.MOVE, pond_object=self.pond_object, to_x=food.pos.x, to_y=food.pos.y
                    )
                else:
                    break

        return self._random_movement_decision()

    def _random_movement_decision(self) -> Decision:
        pos_to_move = self._find_random_pos_to_move()
        return Decision(DecisionType.MOVE, pond_object=self.pond_object, to_x=pos_to_move.x, to_y=pos_to_move.y)

    def _reproduce_decision(self) -> Decision:
        if self.pond_object.vitality > self.pond_object.vitality_need_to_breed:
            print("BREEDING: ", self.pond_object.pos.x, self.pond_object.pos.y)
            return Decision(DecisionType.REPRODUCE, pond_object=self.pond_object)

    @overrides
    def get_decisions(self, pond_viewer: PondViewer) -> DecisionSet:
        decisions = DecisionSet()
        reproduce_decision = self._reproduce_decision()
        decisions.add(reproduce_decision)
        if reproduce_decision is None:
            decisions.add(self._movement_decision(pond_viewer))
        return decisions
