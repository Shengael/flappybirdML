from resources.sprite_path import Sprites
from src.services.arcade_service import FSprite, ArcadeService


class Bird:
    def __init__(self, initial=200, ratio=0.5) -> None:
        self.ratio = ratio
        self.sprite: FSprite = ArcadeService.load_sprite(Sprites.bird, ratio)
        self.sprite.center_y = initial + ratio
        self.sprite.center_x = self.sprite.height * ratio

    def flap(self) -> None:
        print("flap")
        self.sprite.center_y += 10

    def fall(self) -> None:
        print("fall")
        self.sprite.center_y -= 10

    def get_state(self) -> int:
        return int(self.sprite.center_y)

    def get_top(self) -> float:
        return self.sprite.center_y + self.ratio

    def get_bottom(self) -> float:
        return self.sprite.center_y - self.ratio

    def get_position_x(self) -> float:
        return self.sprite.center_x
