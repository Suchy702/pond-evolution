from typing import ClassVar

from src.graphics.image_handler.image_handler import StaticImageHandler


class UIImageHandler(StaticImageHandler):
    img_paths: ClassVar[list[str]] = [
        'arrow.svg', 'arrow2.svg', 'arrow3.svg', 'omnivore_fish.svg', 'magnifying_glass.svg', 'plus.svg'
    ]
