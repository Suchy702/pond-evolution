from __future__ import annotations

from typing import Optional, TYPE_CHECKING, TypeAlias

from src.decision.decision_type import DecisionType

if TYPE_CHECKING:
    from src.object.pond_object import PondObject
from src.object_kind import ObjectKind


class Decision:
    def __init__(
            self, decision_type: DecisionType, pond_object: Optional[PondObject] = None, *,
            to_x: Optional[int] = None,
            to_y: Optional[int] = None,
            how_many: Optional[int] = None,
            kind: Optional[ObjectKind] = None
    ):
        self.decision_type = decision_type
        self.pond_object = pond_object
        self.to_x = to_x
        self.to_y = to_y
        self.how_many = how_many
        self.kind = kind

    def add_to_dict(self, decisions: decisionSetType) -> None:
        if self.decision_type not in decisions:
            decisions[self.decision_type] = {}

        # TODO: dlaczego tu jest warning: local variable not used?
        obj_kind = None
        if self.pond_object is not None:
            obj_kind = self.pond_object.kind
        elif self.kind is not None:
            obj_kind = self.kind
        else:
            raise Exception('Cannot deduce object type')

        if obj_kind not in decisions[self.decision_type]:
            decisions[self.decision_type][obj_kind] = []

        decisions[self.decision_type][obj_kind].append(self)

    @staticmethod
    def combine_decision_dicts(a: decisionSetType, b: decisionSetType) -> None:
        for by_type in a:
            for by_kind in a[by_type]:
                for decision in a[by_type][by_kind]:
                    decision.add_to_dict(b)


decisionSetType: TypeAlias = dict[DecisionType, dict[ObjectKind, list[Decision]]]
