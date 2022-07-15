from __future__ import annotations

from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from src.object.pond_object import PondObject
    from src.decision.decision_type import DecisionType
    from src.object_kind import ObjectKind


class Decision:
    __slots__ = ('decision_type', 'pond_object', 'to_x', 'to_y', 'how_many', 'kind')

    def __init__(
            self, decision_type: DecisionType, *,
            pond_object: Optional[PondObject] = None,
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
