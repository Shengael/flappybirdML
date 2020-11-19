import copy
from typing import Tuple

from resources.env import UP, RELEASE
from src.controllers.board_controller import BoardController
from src.controllers.texture_manager import TextureManager
from src.entities.bird import Bird
from src.enum.reward import Reward


class Environment:
    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self.board_controller = BoardController(width, height)
        self.win_streak = 0
        self.best_win_streak = 0
        self.loose = False
        self.checked = False
        self.texture_manager = TextureManager()

    def reset(self) -> None:
        self.win_streak = 0
        self.best_win_streak = 0
        self.loose = False
        self.checked = False

    def update_bird(self, bird: Bird, action: str) -> Tuple[Bird, int]:
        self.checked = False
        old_bird = copy.deepcopy(bird)
        if action == UP:
            bird.flap()

        reset_bird, reward = self.get_reward(old_bird, bird)

        if reset_bird:
            if action == UP:
                bird.fall()

        return bird, reward

    def get_reward(self, old_bird: Bird, bird: Bird) -> Tuple[bool, int]:
        reset_bird = False
        if bird.get_top() <= self.height and bird.get_bottom() > 0:
            if self.board_controller.is_top(bird):
                print("Is stuck!")
                reward = Reward.REWARD_STUCK
                reset_bird = True
            elif self.board_controller.is_bottom(bird) or self.board_controller.is_pipe(bird):
                print('loose')
                self.loose = True
                reward = Reward.REWARD_LOOSE
                self.board_controller.goals.pop(0)
            elif self.board_controller.is_checkpoint(bird):
                print('win')
                self.win_streak += 1
                self.checked = True
                reward = Reward.REWARD_CHECKPOINT
                self.board_controller.goals.pop(0)
            else:
                reward = Reward.REWARD_DEFAULT
        else:
            print("Is impossible!")
            reset_bird = True
            reward = Reward.REWARD_IMPOSSIBLE

        penalty = 0
        if not reset_bird:
            distance = self.board_controller.distance_next_pipe(bird)
            old_distance = self.board_controller.distance_next_pipe(old_bird)
            if distance == -1:
                penalty = 0
            elif old_distance - distance < 0:
                penalty = distance * int(Reward.REWARD_PENALTY)
            else:
                penalty = int(Reward.REWARD_CHECKPOINT) * 0.05
        return reset_bird, int(reward) + penalty
