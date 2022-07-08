import os.path

import pygame
from overrides import overrides
from pygame.surface import Surface

from src.graphics.image_handler.image_handler import ImageHandler, IMG_DIR_PATH
from src.object.pond_object import PondObject
from src.object_handler.pond_object_handler import PondObjectHandler


class FishImageHandler(ImageHandler):
    def __init__(self, handler: PondObjectHandler):
        super().__init__(handler)
        self._cache = None

    @overrides
    def _get_object_image(self, obj: PondObject) -> Surface:
        if self._cache is None:
            self._cache = pygame.image.load(os.path.join(IMG_DIR_PATH, 'fish.svg'))
        return self._cache
