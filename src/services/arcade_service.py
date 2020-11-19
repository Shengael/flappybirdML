from typing import NewType

import arcade
from arcade import Sprite

FSprite = NewType('Sprite', Sprite)


class ArcadeService:
    @staticmethod
    def load_sprite(path: str, ratio: float):
        return arcade.Sprite(path, ratio)
