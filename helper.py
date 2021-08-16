from RandomAgent import RandomAgent

EVALUATION_EPISODES = 10_000


def evaluate(agent, env):
    agent_random = RandomAgent()

    wins = 0
    loses = 0

    for i in range(EVALUATION_EPISODES):
        state = env.reset()
        while True:
            if env.starts == agent.symbol:
                _, _, done = agent.step(env)
                if done:
                    break

                previous_state, new_state, done = agent_random.step(env)
                if done:
                    break

            else:
                previous_state, new_state, done = agent_random.step(env)
                if done:
                    break

                _, _, done = agent.step(env)
                if done:
                    break

        episode_winner = env.determine_winner()

        if episode_winner == agent.symbol:
            wins += 1
        elif episode_winner != "D":
            loses += 1

    print("Evaluation against random opponent")
    print(f"Win: {wins / EVALUATION_EPISODES * 100}%, "
          f"Lose: {loses / EVALUATION_EPISODES * 100}%, "
          f"Draw: {(EVALUATION_EPISODES - wins - loses) / EVALUATION_EPISODES * 100}%")


def finish_episode(agent_x, agent_o, wins_x, wins_o, i, env, eps_decay):
    episode_winner = env.determine_winner()
    if episode_winner == "O":
        agent_o.wins += 1
        wins_o[i // 1000 - 1] += 1
    if episode_winner == "X":
        agent_x.wins += 1
        wins_x[i // 1000 - 1] += 1

    agent_x.epsilon -= eps_decay
    agent_o.epsilon -= eps_decay

    # change who will start in the next round
    env.toggle_starts()
