from __future__ import annotations

from enum import Enum, auto, unique
from typing import TYPE_CHECKING

from src.object_kind import ObjectKind

if TYPE_CHECKING:
    from src.object.fish import Fish


@unique
class FishType(Enum):
    HERBIVORE = auto()
    CARNIVORE = auto()
    OMNIVORE = auto()

    @staticmethod
    def get_edible_food(fish: Fish) -> list[ObjectKind]:
        match fish.fish_type.name:
            case 'HERBIVORE':
                return [ObjectKind.ALGA]
            case 'CARNIVORE':
                # one needs to have PREDATOR trait to eat other fish
                return [ObjectKind.WORM]
            case 'OMNIVORE':
                return [ObjectKind.ALGA, ObjectKind.WORM]
            case _:
                raise Exception

    def __lt__(self, other):
        return self.value < other.value

    def __eq__(self, other):
        return self.value == other.value

    def __str__(self):
        return self.name
