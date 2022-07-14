from __future__ import annotations

from typing import Optional

from src.decision.decision_type import DecisionType
from src.object.pond_object import PondObject
from src.object_kind import ObjectKind


class Decision:
    def __init__(
            self, decision_type: DecisionType, pond_object: PondObject, *,
            to_x: Optional[int] = None,
            to_y: Optional[int] = None,
            how_many: Optional[int] = None
    ):
        self.decision_type = decision_type
        self.pond_object = pond_object
        self.to_x = to_x
        self.to_y = to_y
        self.how_many = how_many

    def add_to_dict(self, decisions: decisionSetType) -> None:
        if self.decision_type not in decisions:
            decisions[self.decision_type] = {}

        if self.pond_object.kind not in decisions[self.decision_type]:
            decisions[self.decision_type][self.pond_object.kind] = []

        decisions[self.decision_type][self.pond_object.kind].append(self)

    @staticmethod
    def combine_decision_dicts(a: decisionSetType, b: decisionSetType) -> None:
        for by_type in a:
            for by_kind in a[by_type]:
                for decision in a[by_type][by_kind]:
                    decision.add_to_dict(b)


decisionSetType = dict[DecisionType, dict[ObjectKind, list[Decision]]]
