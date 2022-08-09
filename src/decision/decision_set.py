from __future__ import annotations

from src.decision.decision import Decision
from src.decision.decision_type import DecisionType
from src.object.object_kind import ObjectKind


class DecisionSet:
    def __init__(self):
        self.decisions: dict[DecisionType, dict[ObjectKind, list[Decision]]] = {}
        self.decisions_list: list[Decision] = []

    @staticmethod
    def _deduce_object_type(decision: Decision) -> ObjectKind:
        if decision.pond_object is not None:
            return decision.pond_object.kind
        elif decision.kind is not None:
            return decision.kind
        else:
            raise Exception('Cannot deduce object type')

    def _check_decision_type_existing(self, decision_type: DecisionType) -> None:
        if decision_type not in self.decisions:
            self.decisions[decision_type] = {}

    def _check_obj_kind_existing(self, obj_kind: ObjectKind, decision_type: DecisionType) -> None:
        if obj_kind not in self.decisions[decision_type]:
            self.decisions[decision_type][obj_kind] = []

    def _check_safety_off_add(self, decision: Decision, obj_kind: ObjectKind) -> None:
        self._check_decision_type_existing(decision.decision_type)
        self._check_obj_kind_existing(obj_kind, decision.decision_type)

    def add(self, decision: Decision) -> None:
        if decision is None:
            return

        obj_kind = self._deduce_object_type(decision)
        self._check_safety_off_add(decision, obj_kind)
        self.decisions[decision.decision_type][obj_kind].append(decision)
        self.decisions_list.append(decision)

    def __add__(self, other: DecisionSet) -> DecisionSet:
        result = DecisionSet()
        for decision in self.decisions_list + other.decisions_list:
            result.add(decision)
        return result

    def __iadd__(self, other: DecisionSet) -> DecisionSet:
        for decision in other.decisions_list:
            self.add(decision)
        return self

    def _is_item_in_set(self, decision_type: DecisionType, obj_kind: ObjectKind) -> bool:
        return decision_type in self.decisions and obj_kind in self.decisions[decision_type]

    def __getitem__(self, item: tuple[DecisionType, ObjectKind]) -> list[Decision]:
        if self._is_item_in_set(item[0], item[1]):
            return self.decisions[item[0]][item[1]]

        return []
