from enum import IntEnum


class Reward(IntEnum):
    REWARD_LOOSE = -5000
    REWARD_IMPOSSIBLE = -500
    REWARD_STUCK = -10
    REWARD_PENALTY = -2
    REWARD_DEFAULT = -1
    REWARD_CHECKPOINT = 10
