from resources.env import PLAYER_SPEED
from resources.sprite_path import Sprites
from src.services.arcade_service import FSprite, ArcadeService


class Bird:
    def __init__(self, initial=400, ratio=0.5) -> None:
        self.ratio = ratio
        self.sprite: FSprite = ArcadeService.load_sprite(Sprites.bird, ratio)
        self.initial = initial
        self.reset()

    def reset(self):
        self.sprite.center_y = self.initial + self.sprite.height * 0.5
        self.sprite.center_x = self.sprite.width * 0.5
        return self

    def flap(self) -> None:
        self.sprite.center_y += PLAYER_SPEED

    def fall(self) -> None:
        self.sprite.center_y -= PLAYER_SPEED

    def get_state(self) -> int:
        return int(self.sprite.center_y)

    def get_top(self) -> float:
        return self.sprite.center_y + self.sprite.height * 0.5

    def get_bottom(self) -> float:
        return self.sprite.center_y - self.sprite.height * 0.5

    def get_position_x(self) -> float:
        return self.sprite.center_x

    def get_min_x(self) -> float:
        return self.sprite.center_x - self.sprite.width * 0.5

    def get_max_x(self) -> float:
        return self.sprite.center_x + self.sprite.width * 0.5
