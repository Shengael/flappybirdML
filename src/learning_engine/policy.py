from resources.env import DEFAULT_LEARNING_RATE, DEFAULT_DISCOUNT_FACTOR, POSITIONS, ACTIONS, ABOVE, CHEAT_LEARNING


class Policy:  # Q-table
    def __init__(self, states: int,
                 learning_rate=DEFAULT_LEARNING_RATE,
                 discount_factor=DEFAULT_DISCOUNT_FACTOR):
        self.table = {}
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        if CHEAT_LEARNING:
            for p in POSITIONS:
                self.table[p] = {}
                for a in ACTIONS:
                    self.table[p][a] = 0
        else:
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
        if CHEAT_LEARNING:
            for a in self.table[position]:
                if action is None or self.table[position][a] > self.table[position][action]:
                    action = a
        else:
            for a in self.table[state][position]:
                if action is None or self.table[position][a] > self.table[position][action]:
                    action = a
        return action

    def update(self, previous_state: int, state: int, previous_position: str, position: str,
               last_action: str, reward: int) -> None:
        if CHEAT_LEARNING:
            max_q = max(self.table[position].values())
            value = reward + self.discount_factor * max_q - self.table[previous_position][last_action]
            self.table[previous_position][last_action] += self.learning_rate * value
        else:
            max_q = max(self.table[state][position].values())
            value = reward + self.discount_factor * max_q - self.table[previous_state][previous_position][last_action]
            self.table[previous_state][previous_position][last_action] += self.learning_rate * value

