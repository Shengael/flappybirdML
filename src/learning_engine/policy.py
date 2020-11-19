from resources.env import DEFAULT_LEARNING_RATE, DEFAULT_DISCOUNT_FACTOR
from src.enum.position import Position


class Policy:  # Q-table
    def __init__(self, states, actions,
                 learning_rate=DEFAULT_LEARNING_RATE,
                 discount_factor=DEFAULT_DISCOUNT_FACTOR):
        self.table = {}
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        for s in states:
            self.table[s] = {}
            for p in Position:
                self.table[s][p.value] = {}
                for a in actions:
                    self.table[s][p.value][a] = 0

    def __repr__(self):
        res = ''
        for state in self.table:
            res += f'{state}\t{self.table[state]}\n'
        return res

    def best_action(self, state, position):
        action = None
        for a in self.table[state][position]:
            if action is None or self.table[state][position][a] > self.table[state][position][action]:
                action = a
        return action

    def update(self, previous_state, state, previous_position, position, last_action, reward):
        # Q(st, at) = Q(st, at) + learning_rate * (reward + discount_factor * max(Q(state)) - Q(st, at))
        maxQ = max(self.table[state][position].values())
        self.table[previous_state][previous_position][last_action] += self.learning_rate * \
                                                                      (reward + self.discount_factor * maxQ -
                                                                       self.table[previous_state][previous_position][
                                                                           last_action])