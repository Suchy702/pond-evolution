import os.path

import pygame
from overrides import overrides
from pygame.surface import Surface

from src.graphics.image_handler.image_handler import ImageHandler, IMG_DIR_PATH
from src.object.pond_object import PondObject


class FishImageHandler(ImageHandler):
    _cache: Surface = None

    @staticmethod
    @overrides
    def get_object_image(obj: PondObject) -> Surface:
        if FishImageHandler._cache is None:
            FishImageHandler._cache = pygame.image.load(os.path.join(IMG_DIR_PATH, 'fish.svg')).convert_alpha()
        return FishImageHandler._cache
