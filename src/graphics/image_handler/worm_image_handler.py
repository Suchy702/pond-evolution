from typing import ClassVar

from overrides import overrides

from src.graphics.image_handler.image_handler import DynamicImageHandler
from src.object.pond_object import PondObject


class WormImageHandler(DynamicImageHandler):
    image_paths: ClassVar[list[str]] = ['worm.svg']

    @overrides
    def _choose_image(self, object_: PondObject) -> str:
        return self.image_paths[0]
