from resources.env import SCREEN_HEIGHT


class Pipe:
    def __init__(self, bottom: int, top: int, position_x):
        self.bottom = bottom
        self.top = top
        self.height_top = SCREEN_HEIGHT - self.top
        self.height_bottom = self.bottom
        self.center_y = (self.top + self.bottom) / 2
        self.position_x = position_x
