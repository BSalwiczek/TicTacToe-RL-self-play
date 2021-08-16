from helper import evaluate, finish_episode
from Agent import Agent
from RandomAgent import RandomAgent
from TicTacToe import TicTacToe
import matplotlib.pyplot as plt

MODE = 'ONE-SELF-PLAY'  # 'RANDOM', 'TWO-SELF-PLAY', 'ONE-SELF-PLAY'

EPSILON_DECAY = 0.00001
EPISODES = 200_000

agent_x = Agent("X")
agent_o = Agent("O")
agent_random = RandomAgent()

env = TicTacToe("X")

values_x = {}
values_o = {}
env.generate_values_tables("", values_x, values_o)
agent_x.values = values_x
agent_o.values = values_o

wins_x = [0] * (EPISODES//1000-1)
wins_o = [0] * (EPISODES//1000-1)


if MODE == 'RANDOM':
    # Train against random agent
    for i in range(EPISODES):
        if i % 1000 == 0:
            print(i)
        state = env.reset()
        while True:
            if env.starts == "X":
                _, _, done = agent_x.step(env)
                if done:
                    break

                previous_state, new_state, done = agent_random.step(env)
                agent_x.update(previous_state, new_state)
                if done:
                    break

            else:
                previous_state, new_state, done = agent_random.step(env)
                agent_x.update(previous_state, new_state)
                if done:
                    break

                _, _, done = agent_x.step(env)
                if done:
                    break

        finish_episode(agent_x, agent_o, wins_x, wins_o, i, env, EPSILON_DECAY)

if MODE == 'TWO-SELF-PLAY':
    # Train two agents against themselves
    for i in range(EPISODES):
        if i % 1000 == 0:
            print(i)
        state = env.reset()
        while True:
            if env.starts == "X":
                previous_state, new_state, done = agent_x.step(env)
                agent_o.update(previous_state, new_state)
                if done:
                    break

                previous_state, new_state, done = agent_o.step(env)
                agent_x.update(previous_state, new_state)
                if done:
                    break

            else:
                previous_state, new_state, done = agent_o.step(env)
                agent_x.update(previous_state, new_state)
                if done:
                    break

                previous_state, new_state, done = agent_x.step(env)
                agent_o.update(previous_state, new_state)
                if done:
                    break

        finish_episode(agent_x, agent_o, wins_x, wins_o, i, env, EPSILON_DECAY)


if MODE == 'ONE-SELF-PLAY':
    # Train one agent against itself
    for i in range(EPISODES):
        if i % 1000 == 0:
            print(i)
        state = env.reset()
        while True:
            if env.starts == "X":
                previous_state, new_state, done = agent_x.step(env)
                if done:
                    break

                env.swap_o_and_x()
                previous_state, new_state, done = agent_x.step(env)
                env.swap_o_and_x()
                if done:
                    break

            else:
                env.swap_o_and_x()
                previous_state, new_state, done = agent_x.step(env)
                env.swap_o_and_x()
                if done:
                    break

                previous_state, new_state, done = agent_x.step(env)
                if done:
                    break

        finish_episode(agent_x, agent_o, wins_x, wins_o, i, env, EPSILON_DECAY)

print(f"X: {agent_x.wins}, O: {agent_o.wins}, Draw: {EPISODES - agent_x.wins - agent_o.wins}")
plt.plot(range(0,EPISODES-1000,1000),[wins_x[i]-wins_o[i] for i, x in enumerate(wins_x)])
plt.grid(True)
plt.ylim(-1000,1000)
plt.title("Agent learning results (every 1000 episodes)")
plt.ylabel("Advantage of victories")
plt.xlabel("Episode")
plt.show()

agent_x.epsilon = 0
evaluate(agent_x,env)