import arcade
import random

UP, RELEASE = 'U', 'R'
ACTIONS = [UP, RELEASE]
ABOVE, IN, UNDER, NO_PIPE = 'A', 'I', 'N', 'P'
POSITIONS = [ABOVE, IN, UNDER, NO_PIPE]
MAZE = """
###############################
                               
 .                             
                               
                               
                               
                               
                               
                               
                               
                               
_______________________________
"""
REWARD_LOOSE = -10000
REWARD_IMPOSSIBLE = -60
REWARD_STUCK = -1000
REWARD_PENALTY = -200
REWARD_DEFAULT = -1
REWARD_CHECKPOINT = 1500
REWARD_GOAL = 60
DEFAULT_LEARNING_RATE = 1
DEFAULT_DISCOUNT_FACTOR = 0.5
SPRITE_SIZE = 64
PIPE_FREQUENCY = 15
MIN_PIPE_SIZE = 1
GAP_SIZE = 3


class Environment:

    def __init__(self, text):
        self.goals = []
        self.width = 0
        self.height = 0
        self.win_streak = 0
        self.best_win_streak = 0
        self.frequency = PIPE_FREQUENCY
        self.loose = False
        self.checked = False
        self.states = {}
        self.starting_point = None
        self.initial = text
        self.reset()

    def reset(self):
        self.states = {}
        self.goals = []
        self.loose = False
        self.checked = False
        self.win_streak = 0
        self.frequency = PIPE_FREQUENCY
        lines = self.initial.strip().split('\n')
        self.height = len(lines)
        self.width = len(lines[0])
        for row in range(self.height):
            for col in range(self.width):
                self.states[(row, col)] = lines[row][col]
                if lines[row][col] == '.':
                    self.starting_point = (row, col)
        return self.starting_point

    def check_pipe(self):
        self.frequency -= 1

        for row in range(self.height - 1):
            for col in range(self.width - 1):
                self.states[(row, col)] = self.states[(row, col + 1)]

        for goal in self.goals:
            goal["x"] -= 1

        if self.frequency != 0:
            for i in range(1, self.height - 1):
                self.states[(i, self.width - 1)] = ' '
        else:
            self.frequency = PIPE_FREQUENCY
            top_pipe = random.randint(MIN_PIPE_SIZE + 1, self.height - 1 - MIN_PIPE_SIZE - GAP_SIZE)
            bottom_pipe = top_pipe + GAP_SIZE
            self.goals.append({"top": top_pipe, "bottom": bottom_pipe, "x": self.width - 1})

            self.states[(top_pipe, self.width - 1)] = '&'
            self.states[(bottom_pipe, self.width - 1)] = '&'

            for i in range(self.height - 1):
                if 1 <= i < top_pipe:
                    self.states[(i, self.width - 1)] = '@'
                elif bottom_pipe < i <= self.height:
                    self.states[(i, self.width - 1)] = '@'
                elif top_pipe < i < bottom_pipe:
                    self.states[(i, self.width - 1)] = '+'

    def distance(self, state):
        if len(self.goals) == 0:
            return -1
        if state[0] <= self.goals[0]['top']:
            return self.goals[0]['top'] - state[0] + 1
        if state[0] >= self.goals[0]['bottom']:
            return state[0] - self.goals[0]['bottom'] + 1
        return 0

    def in_checkpoint(self, state):
        if len(self.goals) == 0:
            return False
        if self.goals[0]["x"] == state[1] and self.goals[0]["top"] < state[0] < self.goals[0]["bottom"]:
            return True
        return False

    def position(self, state):
        if len(self.goals) == 0:
            return NO_PIPE
        if state[0] <= self.goals[0]['top']:
            return ABOVE
        if state[0] >= self.goals[0]['bottom']:
            return UNDER
        return IN

    def apply(self, state, action):
        self.checked = False
        new_state = None
        if action == UP:
            new_state = (state[0] - 1, state[1])
        elif action == RELEASE:
            new_state = (state[0] + 1, state[1])
        reward = 0
        if new_state in self.states:
            if self.states[new_state] in ['#']:
                new_state = state
                reward += REWARD_STUCK
            if self.states[new_state] in ['_', '@', '&']:
                print('loose')
                self.loose = True
                reward += REWARD_LOOSE
            elif self.in_checkpoint(new_state):
                print('win')
                self.win_streak += 1
                self.checked = True
                reward += REWARD_CHECKPOINT
                self.goals.pop(0)
            else:
                reward += REWARD_DEFAULT
        else:
            new_state = state
            reward += REWARD_IMPOSSIBLE

        distance = self.distance(new_state)
        old_distance = self.distance(state)
        if distance == -1:
            penalty = 0
        elif old_distance - distance < 0:
            penalty = distance * REWARD_PENALTY
        else:
            penalty = REWARD_CHECKPOINT

        return new_state, reward + penalty


class Agent:

    def __init__(self, env):
        self.environment = env
        self.policy = Policy(env.states.keys(), ACTIONS)
        self.reset()

    def reset(self):
        self.state = self.environment.reset()
        self.previous_state = self.state
        self.score = 0

    def best_action(self):
        return self.policy.best_action(self.state, self.environment.position(self.state))

    def do(self, action):
        self.previous_state = self.state
        #
        self.state, self.reward = self.environment.apply(self.state, action)
        self.score += self.reward
        self.last_action = action

    def update_policy(self):
        self.policy.update(self.previous_state, self.state, self.environment.position(self.previous_state),
                           self.environment.position(self.state), self.last_action, self.reward)


class Policy:  # Q-table
    def __init__(self, states, actions,
                 learning_rate=DEFAULT_LEARNING_RATE,
                 discount_factor=DEFAULT_DISCOUNT_FACTOR):
        self.table = {}
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        for s in states:
            self.table[s] = {}
            for p in POSITIONS:
                self.table[s][p] = {}
                for a in actions:
                    self.table[s][p][a] = 0

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


class MazeWindow(arcade.Window):
    def __init__(self, agent):
        super().__init__(agent.environment.width * SPRITE_SIZE,
                         agent.environment.height * SPRITE_SIZE,
                         "Escape from ESGI")
        self.agent = agent

    def setup(self):
        self.walls = arcade.SpriteList()

        for state in agent.environment.states:
            if agent.environment.states[state] == '#':
                sprite = arcade.Sprite(":resources:images/tiles/grassCenter.png", 0.5)
                sprite.center_x = sprite.width * (state[1] + 0.5)
                sprite.center_y = sprite.height * (agent.environment.height - state[0] - 0.5)
                self.walls.append(sprite)
            if agent.environment.states[state] == '@':
                sprite = arcade.Sprite(":resources:images/enemies/slimeBlock.png", 0.5)
                sprite.center_x = sprite.width * (state[1] + 0.5)
                sprite.center_y = sprite.height * (agent.environment.height - state[0] - 0.5)
                self.walls.append(sprite)
            if agent.environment.states[state] == '&':
                sprite = arcade.Sprite(":resources:images/tiles/stoneCenter_rounded.png", 0.5)
                sprite.center_x = sprite.width * (state[1] + 0.5)
                sprite.center_y = sprite.height * (agent.environment.height - state[0] - 0.5)
                self.walls.append(sprite)
            if agent.environment.states[state] == '_':
                sprite = arcade.Sprite(":resources:images/tiles/waterTop_high.png", 0.5)
                sprite.center_x = sprite.width * (state[1] + 0.5)
                sprite.center_y = sprite.height * (agent.environment.height - state[0] - 0.5)
                self.walls.append(sprite)

        self.player = arcade.Sprite(":resources:images/animated_characters/male_adventurer/maleAdventurer_walk1.png",
                                    0.5)
        self.update_player_xy()

    def update_player_xy(self):
        self.player.center_x = self.player.height * (self.agent.state[1] + 0.5)
        self.player.center_y = self.player.height * (agent.environment.height - self.agent.state[0] - 0.5)

    def on_update(self, delta_time):
        action = self.agent.best_action()
        self.setup()
        self.agent.environment.check_pipe()
        self.agent.do(action)
        self.agent.update_policy()
        self.update_player_xy()
        if self.agent.environment.loose:
            if  self.agent.environment.best_win_streak < self.agent.environment.win_streak:
                self.agent.environment.best_win_streak = self.agent.environment.win_streak
            self.agent.reset()
        if self.agent.environment.checked:
            self.agent.score = 0

    def on_draw(self):
        arcade.start_render()

        self.walls.draw()
        self.player.draw()

        arcade.draw_text(f"Win streak: {self.agent.environment.win_streak}", 10,
                         (self.agent.environment.height - 0.5) * self.player.height - 10, arcade.csscolor.GREEN, 20)
        arcade.draw_text(f"best Win streak: {self.agent.environment.best_win_streak}", 300,
                         (self.agent.environment.height - 0.5) * self.player.height - 10, arcade.csscolor.BLUE, 20)

        arcade.draw_text(f"Score: {self.agent.score}", 10, 10, arcade.csscolor.BLACK, 20)


if __name__ == "__main__":
    # Initialiser l'environment
    environment = Environment(MAZE)

    # Initialiser l'agent
    agent = Agent(environment)

    # Lancer le jeu
    window = MazeWindow(agent)
    window.setup()
    arcade.run()
