from __future__ import annotations

from typing import Optional

from src.decision.decision_type import DecisionType


class Decision:
    def __init__(
            self, decision_type: DecisionType, *,
            to_x: Optional[int] = None,
            to_y: Optional[int] = None,
            how_many: Optional[int] = None
    ):
        self.decision_type = decision_type
        self.to_x = to_x
        self.to_y = to_y
        self.how_many = how_many

    def add_to_dict(self, decisions: dict[DecisionType, list[Decision]]) -> None:
        if self.decision_type not in decisions:
            decisions[self.decision_type] = []

        decisions[self.decision_type].append(self)
