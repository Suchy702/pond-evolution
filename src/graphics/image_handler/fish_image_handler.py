from typing import ClassVar, cast

from overrides import overrides

from src.graphics.image_handler.image_handler import DynamicImageHandler
from src.object.fish import Fish
from src.object.fish_trait import FishTrait
from src.object.pond_object import PondObject


class FishImageHandler(DynamicImageHandler):
    image_paths: ClassVar[list[str]] = [
        'carnivore_fish.svg', 'herbivore_fish.svg', 'omnivore_fish.svg', 'predator_fish.svg'
    ]

    @overrides
    def _choose_image(self, object_: PondObject) -> str:
        fish = cast(Fish, object_)
        if FishTrait.PREDATOR in fish.traits:
            return self.image_paths[3]

        match fish.fish_type.name:
            case 'CARNIVORE':
                return self.image_paths[0]
            case 'HERBIVORE':
                return self.image_paths[1]
            case 'OMNIVORE':
                return self.image_paths[2]
            case _:
                raise Exception
