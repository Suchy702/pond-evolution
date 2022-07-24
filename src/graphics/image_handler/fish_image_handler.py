from typing import ClassVar, cast

from overrides import overrides

from src.graphics.image_handler.image_handler import ImageHandler
from src.object.fish import Fish
from src.object.fish_trait import FishTrait
from src.object.pond_object import PondObject


class FishImageHandler(ImageHandler):
    img_paths: ClassVar[list[str]] = [
        'carnivore_fish.svg', 'herbivore_fish.svg', 'omnivore_fish.svg', 'predator_fish.svg'
    ]

    @overrides
    def _choose_image(self, obj: PondObject) -> str:
        fish = cast(Fish, obj)
        if FishTrait.PREDATOR in fish.traits:
            return self.img_paths[3]

        match fish.fish_type.name:
            case 'CARNIVORE':
                return self.img_paths[0]
            case 'HERBIVORE':
                return self.img_paths[1]
            case 'OMNIVORE':
                return self.img_paths[2]
            case _:
                raise Exception
