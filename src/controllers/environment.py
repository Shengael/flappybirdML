import copy
from typing import Tuple

from src.controllers.board_controller import BoardController
from src.enum.action import Action
from src.entities.bird import Bird
from src.enum.reward import Reward


class Environment:
    def __init__(self, width: int, height: int) -> None:
        self.board_controller = BoardController(width, height)
        self.win_streak = 0
        self.best_win_streak = 0
        self.loose = False
        self.checked = False

    def reset(self) -> None:
        self.board_controller.board.reset()
        self.win_streak = 0
        self.best_win_streak = 0
        self.loose = False
        self.checked = False

    def update_bird(self, bird: Bird, action: Action) -> Tuple[Bird, int]:
        self.checked = False
        new_bird = copy.deepcopy(bird)
        if action == Action.UP:
            new_bird.flap()
        elif action == Action.RELEASE:
            new_bird.fall()

        reset_bird, reward = self.get_reward(bird, new_bird)

        if reset_bird:
            new_bird = bird

        return new_bird, reward

    def get_reward(self, old_bird: Bird, bird: Bird) -> Tuple[bool, int]:
        reset_bird = False
        if bird.get_state() in self.board_controller.board.states:
            if self.board_controller.is_top(bird):
                reward = Reward.REWARD_STUCK
                reset_bird = True
            elif self.board_controller.is_bottom(bird) or self.board_controller.is_pipe(bird):
                print('loose')
                self.loose = True
                reward = Reward.REWARD_LOOSE
            elif self.board_controller.is_checkpoint(bird):
                print('win')
                self.win_streak += 1
                self.checked = True
                reward = Reward.REWARD_CHECKPOINT
                self.board_controller.goals.pop(0)
            else:
                reward = Reward.REWARD_DEFAULT
        else:
            reset_bird = True
            reward = Reward.REWARD_IMPOSSIBLE

        distance = self.board_controller.distance_next_pipe(bird)
        old_distance = self.board_controller.distance_next_pipe(old_bird)
        if distance == -1:
            penalty = 0
        elif old_distance - distance < 0:
            penalty = distance * int(Reward.REWARD_PENALTY)
        else:
            penalty = int(Reward.REWARD_CHECKPOINT)

        return reset_bird, int(reward) + penalty
