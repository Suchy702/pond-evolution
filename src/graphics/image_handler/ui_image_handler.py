from typing import ClassVar

from src.graphics.image_handler.image_handler import StaticImageHandler


class UIImageHandler(StaticImageHandler):
    img_paths: ClassVar[list[str]] = [
        'adding_obejct_description.svg', 'behaviour_description.svg', 'control_description.svg', 'cycle.svg'
    ]
