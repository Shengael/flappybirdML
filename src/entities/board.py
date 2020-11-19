from resources.flappy_types import States, Goals


class Board:
    def __init__(self, width: int, height: int) -> None:
        self.states: States = Board.create_states(self.width, self.height)
        self.width: int = width
        self.height: int = height

    def reset(self) -> None:
        self.states = Board.create_states(self.width, self.height)

    @staticmethod
    def create_states(width: int, height: int) -> States:
        return {(y, x): ' ' for y in range(height) for x in range(width)}
