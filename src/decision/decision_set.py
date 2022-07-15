from __future__ import annotations

from src.decision.decision import Decision
from src.decision.decision_type import DecisionType
from src.object_kind import ObjectKind


class DecisionSet:
    def __init__(self):
        self.decisions: dict[DecisionType, dict[ObjectKind, list[Decision]]] = {}

    def add(self, decision: Decision) -> None:
        if decision.decision_type not in self.decisions:
            self.decisions[decision.decision_type] = {}

        # TODO: dlaczego tu jest warning: local variable not used?
        obj_kind = None
        if decision.pond_object is not None:
            obj_kind = decision.pond_object.kind
        elif decision.kind is not None:
            obj_kind = decision.kind
        else:
            raise Exception('Cannot deduce object type')

        if obj_kind not in self.decisions[decision.decision_type]:
            self.decisions[decision.decision_type][obj_kind] = []

        self.decisions[decision.decision_type][obj_kind].append(decision)

    def __add__(self, other: DecisionSet) -> DecisionSet:
        result = DecisionSet()
        for by_type in self.decisions:
            for by_kind in self.decisions[by_type]:
                for decision in self.decisions[by_type][by_kind]:
                    result.add(decision)

        for by_type in other.decisions:
            for by_kind in other.decisions[by_type]:
                for decision in other.decisions[by_type][by_kind]:
                    result.add(decision)

        return result

    def __iadd__(self, other: DecisionSet) -> DecisionSet:
        for by_type in other.decisions:
            for by_kind in other.decisions[by_type]:
                for decision in other.decisions[by_type][by_kind]:
                    self.add(decision)
        return self

    def __getitem__(self, item: tuple[DecisionType, ObjectKind]) -> list[Decision]:
        if item[0] in self.decisions and item[1] in self.decisions[item[0]]:
            return self.decisions[item[0]][item[1]]

        return []
