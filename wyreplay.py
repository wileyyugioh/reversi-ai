# https://medium.freecodecamp.org/deep-reinforcement-learning-where-to-start-291fb0058c01

import numpy as np


empty = 0
black = 1
white = -1


class Replay:
    def __init__(self, gamma=.9):
        self._gamma = gamma
        self._memory = []

    def remember(self, state, game_over):
        self._memory.append([state, game_over])

    def clear(self):
        self._memory = []

    def get_batch(self, model, batch_size):

        len_memory = len(self._memory)

        num_actions = model.output_shape[-1]

        len_inputs = min(len_memory, batch_size)

        board_in = np.zeros((len_inputs, 64))
        color_in = np.zeros((len_inputs, 1))

        targets = np.zeros((len_inputs, num_actions))

        for i, idx in enumerate(range(len(self._memory) - 1, -1, -1)):
            state_t, action_t, reward_t, state_f = self._memory[idx][0]

            game_over = self._memory[idx][1]

            board_in[i:i+1] = state_t[0]
            color_in[i:i+1] = state_t[1]

            targets[i] = model.predict(state_t)[0]

            if game_over:
                targets[i, action_t] = reward_t
            else:
                # Since we are backwards propagating
                future_reward = self._memory[idx + 1][0][2] * self._gamma
                self._memory[idx][0][2] = future_reward
                targets[i, action_t] = reward_t + future_reward

        return board_in, color_in, targets
