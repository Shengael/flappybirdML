from resources.env import DEFAULT_LEARNING_RATE, DEFAULT_DISCOUNT_FACTOR, POSITIONS, ACTIONS


class Policy:  # Q-table
    def __init__(self, states: int,
                 learning_rate=DEFAULT_LEARNING_RATE,
                 discount_factor=DEFAULT_DISCOUNT_FACTOR):
        self.table = {}
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        for s in range(states):
            self.table[s] = {}
            for p in POSITIONS:
                self.table[s][p] = {}
                for a in ACTIONS:
                    self.table[s][p][a] = 0

    def __repr__(self):
        res = ''
        for state in self.table:
            res += f'{state}\t{self.table[state]}\n'
        return res

    def best_action(self, state: int, position: str) -> str:
        action = None
        for a in self.table[state][position]:
            if action is None or self.table[state][position][a] > self.table[state][position][action]:
                action = a
        return action

    def update(self, previous_state: int, state: int, previous_position: str, position: str,
               last_action: str, reward: int) -> None:
        max_q = max(self.table[state][position].values())
        value = reward + self.discount_factor * max_q - self.table[previous_state][previous_position][last_action]
        self.table[previous_state][previous_position][last_action] += self.learning_rate * value
