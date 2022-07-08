import os.path

import pygame
from overrides import overrides
from pygame.surface import Surface

from src.graphics.image_handler.image_handler import ImageHandler, IMG_DIR_PATH
from src.object.alga import Alga
from src.object.alga_maker import AlgaMaker
from src.object.pond_object import PondObject
from src.object_handler.pond_object_handler import PondObjectHandler


class PlantImageHandler(ImageHandler):
    def __init__(self, handler: PondObjectHandler):
        super().__init__(handler)
        self._alga_maker_cache = None
        self.alga_cache = None

    @overrides
    def _get_object_image(self, obj: PondObject) -> Surface:
        if self._alga_maker_cache is None:
            self._alga_maker_cache = pygame.image.load(os.path.join(IMG_DIR_PATH, 'seaweed.svg'))
        if self.alga_cache is None:
            self._alga_cache = pygame.image.load(os.path.join(IMG_DIR_PATH, 'alga.svg'))

        if isinstance(obj, AlgaMaker):
            return self._alga_maker_cache
        elif isinstance(obj, Alga):
            return self._alga_cache
        else:
            raise Exception('Unknown object type')
