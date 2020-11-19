import random


class RandomService:
    @staticmethod
    def randint(min: int, max: int) -> int:
        return random.randint(min, max)