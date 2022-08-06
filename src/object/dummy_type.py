from __future__ import annotations

from enum import unique, Enum, auto


@unique
class DummyType(Enum):
    FISH_HERBIVORE = auto()
    FISH_CARNIVORE = auto()
    FISH_OMNIVORE = auto()
    FISH_PREDATOR = auto()
    WORM = auto()
    ALGA = auto()
    ALGA_MAKER = auto()
