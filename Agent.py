import random

ALFA = 0.5
EPSILON = 0.99


class Agent:
    def __init__(self, symbol):
        self.values = {}
        self.symbol = symbol
        self.alfa = ALFA
        self.epsilon = EPSILON
        self.wins = 0

    def update(self, previous_state, current_state):
        self.values[previous_state] = self.values[previous_state] + self.alfa * (
                    self.values[current_state] - self.values[previous_state])

    def step(self, env):
        state = env.state
        action, update = self.act(state, env.get_possible_moves())
        new_state, _, done = env.step(action)

        # if update:
        self.update(state, new_state)

        return state, new_state, done

    def act(self, state, possible_moves):
        update = True
        if random.random() < self.epsilon:
            action = random.choice(possible_moves)
            # don't update values when random action chosen
            update = False
        else:
            max_value = -1
            action = -1
            for i in possible_moves:
                possible_state = list(state)
                possible_state[i] = self.symbol
                possible_state = ''.join(possible_state)
                if max_value < self.values[possible_state]:
                    max_value = self.values[possible_state]
                    action = i

        return action, update
