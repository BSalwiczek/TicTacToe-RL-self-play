class TicTacToe:
    def __init__(self, starts):
        self.state = 9 * " "
        self.turn = starts
        self.starts = starts

    def reset(self):
        self.state = 9 * " "
        self.turn = self.starts
        return self.state

    def step(self, action):
        if action in self.get_possible_moves():
            new_state = list(self.state)
            new_state[action] = self.turn
            self.state = ''.join(new_state)

        done = False
        reward = 0

        winner = self.determine_winner()

        if winner != -1:
            done = True

        if winner == self.turn:
            # you won!
            reward = 1
        elif winner not in ['D', -1]:
            # you lose!
            reward = -1

        self.turn = "X" if self.turn == "O" else "O"

        return self.state, reward, done

    def get_possible_moves(self):
        return [i for i, sym in enumerate(self.state) if sym == " "]

    def toggle_starts(self):
        if self.starts == "X":
            self.starts = "O"
        else:
            self.starts = "X"

    def swap_o_and_x(self):
        self.state = self.state.replace("X", "p").replace("O", "X").replace("p", "O")
        self.turn = self.starts

    def render(self):
        print(self.state[:3])
        print(self.state[3:6])
        print(self.state[6:9])

    def determine_winner(self):
        # all possible winning combinations
        winning_combinations = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]

        for combination in winning_combinations:
            if all(self.state[i] == "X" for i in combination):
                return "X"
            if all(self.state[i] == "O" for i in combination):
                return "O"

        if self.state.find(" ") == -1:
            return "D"

        return -1 # no winner yet

    def generate_values_tables(self, partial_state, values_x, values_o):
        if len(partial_state) == 9:
            self.state = partial_state
            winner = self.determine_winner()
            if winner == "X":
                values_x[partial_state] = 1
                values_o[partial_state] = 0
            elif winner == "O":
                values_x[partial_state] = 0
                values_o[partial_state] = 1
            else:
                values_x[partial_state] = 0.5
                values_o[partial_state] = 0.5
            return

        partial_state += " "
        self.generate_values_tables(partial_state, values_x, values_o)
        partial_state = partial_state[:-1]

        partial_state += "X"
        self.generate_values_tables(partial_state, values_x, values_o)
        partial_state = partial_state[:-1]

        partial_state += "O"
        self.generate_values_tables(partial_state, values_x, values_o)
        partial_state = partial_state[:-1]
