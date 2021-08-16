import random


class RandomAgent:

    def step(self, env):
        state = env.state
        action = random.choice(env.get_possible_moves())
        new_state, _, done = env.step(action)
        return state, new_state, done
