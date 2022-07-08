from __future__ import annotations

import os.path
from abc import ABC, abstractmethod

from pygame.surface import Surface

from src.object.pond_object import PondObject
from src.object_handler.pond_object_handler import PondObjectHandler
from src.position import Position

IMG_DIR_PATH = os.path.join('resources', 'object_images')


class ImageHandler(ABC):
    def __init__(self, handler: PondObjectHandler):
        self._handler = handler

    def get_images_at_spot(self, pos: Position):
        images = []
        for obj in self._handler.get_spot_obj(pos):
            images.append(self._get_object_image(obj))
        return images

    @abstractmethod
    def _get_object_image(self, obj: PondObject) -> Surface:
        pass
