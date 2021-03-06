from typing import ClassVar

from overrides import overrides

from src.graphics.image_handler.image_handler import DynamicImageHandler
from src.object.pond_object import PondObject


class WormImageHandler(DynamicImageHandler):
    img_paths: ClassVar[list[str]] = ['worm.svg']

    @overrides
    def _choose_image(self, obj: PondObject) -> str:
        return self.img_paths[0]
