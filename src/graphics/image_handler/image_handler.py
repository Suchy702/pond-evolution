from __future__ import annotations

import os.path
from abc import ABC, abstractmethod

from pygame.surface import Surface

from src.object.pond_object import PondObject

IMG_DIR_PATH = os.path.join('resources', 'object_images')


class ImageHandler(ABC):

    @staticmethod
    @abstractmethod
    def get_object_image(obj: PondObject) -> Surface:
        pass
