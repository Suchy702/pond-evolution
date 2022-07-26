from typing import ClassVar

from overrides import overrides

from src.graphics.image_handler.image_handler import DynamicImageHandler
from src.object.alga import Alga
from src.object.alga_maker import AlgaMaker
from src.object.pond_object import PondObject


class PlantImageHandler(DynamicImageHandler):
    img_paths: ClassVar[list[str]] = ['seaweed.svg', 'alga.svg']

    @overrides
    def _choose_image(self, obj: PondObject) -> str:
        if isinstance(obj, Alga):
            return self.img_paths[1]
        elif isinstance(obj, AlgaMaker):
            return self.img_paths[0]
        else:
            raise Exception('Incorrect object type')
