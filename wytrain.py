from wygameboard import Board
from wymodel import baseline_model
from wyreplay import Replay

import numpy as np
from keras.models import load_model
import tensorflow as tf

from copy import deepcopy
from queue import Queue
from random import choice, random
from threading import Thread, Lock


DEBUG = False
EPSILON = .1
EPOCHS = 10**7
BATCH_SIZE = 128
FILENAME = "reversi3.h5"
THREADS = 8


empty = 0
black = 1
white = -1


if DEBUG:
    from os import system


class AtomicWeights:
    def __init__(self, data=None):
        self._mutex = Lock()
        self._data = data

    def set(self, data):
        with self._mutex:
            self._data = data

    def get(self):
        with self._mutex:
            return deepcopy(self._data)


def update_screen(board):
    system('clear')
    print(board)


class ColorRemember:
    def __init__(self):
        self._mem = [[],[]]
        self._act = [[],[]]
        self._mm = 1

    def _add(self, index, state, action):
        self._mem[index].append(state)
        self._act[index].append(action)

        if len(self._mem[index]) > self._mm:
            del self._mem[index][0]

        if len(self._act[index]) > self._mm:
            del self._act[index][0]

    def remember(self, state, action, color):
        if color == black:
            self._add(0, state, action)
        else:
            self._add(1, state, action)

    def get(self, color):
        if color == black:
            if len(self._mem[0]) >= self._mm:
                return self._mem[0], self._act[0][0]
        else:
            if len(self._mem[1]) >= self._mm:
                return self._mem[1], self._act[1][0]
        return None, None


def train_self(weights, queue, epochs, thread_num):
    remember = Replay()

    with tf.Session(graph = tf.Graph()) as sess:
        target_model = baseline_model()
        target_model.set_weights(weights.get())

        for e in range(epochs + 1):
            remember.clear()
            board = Board()
            cr = ColorRemember()

            game_over = False
            force_random = False
            color = black

            input_t = [np.array(board.get_state(), ndmin=2), np.array([color])]

            while not game_over:
                input_past = input_t

                if DEBUG:
                    update_screen(board)

                if random() <= EPSILON or force_random:
                    action = choice(board.get_valid_moves(color))
                    force_random = False
                else:
                    q = target_model.predict(input_past)
                    if color == black:
                        action = np.argmax(q[0])
                    else:
                        action = np.argmin(q[0])
                try:
                    board.update(action, color)
                except:
                    force_random = True
                    continue

                if board.has_valid_move(-color):
                    color = -color
                elif board.has_valid_move(color):
                    pass
                else:
                    game_over = True

                input_t = [np.array(board.get_state(), ndmin=2), np.array([color])]

                cr.remember(deepcopy(input_past), action, input_past[1][0])

                reward = 0
                if game_over:
                    score = board.score()
                    if score[0] > score[1]:
                        reward = 1
                    elif score[0] < score[1]:
                        reward = -1

                    potential_memory, potential_action = cr.get(input_t[1][0])
                    remember.remember([deepcopy(potential_memory[0]), potential_action, reward, deepcopy(input_t)], game_over)
                    boards, colors, targets = remember.get_batch(target_model, batch_size=BATCH_SIZE)
                    queue.put(([boards, colors], targets))
                    break

                potential_memory, potential_action = cr.get(input_t[1][0])
                if potential_memory:
                    remember.remember([deepcopy(potential_memory[0]), potential_action, reward, deepcopy(input_t)], game_over)

            if e % 1 == 0 and thread_num == 0:
                print("Finished game {}".format(e))
                return

            if e % 100 == 0:
                target_model.set_weights(weights.get())


if __name__ == "__main__":
    try:
        model = load_model(FILENAME)
    except:
        model = baseline_model()

    thread_store = []
    queue = Queue()
    aw = AtomicWeights()
    aw.set(model.get_weights())

    for x in range(THREADS):
        t = Thread(target=train_self, args=(aw, queue, EPOCHS, x,))
        t.daemon = True
        t.start()
        thread_store.append(t)

    for i in range(THREADS * EPOCHS):
        item = queue.get()

        model.train_on_batch(item[0], item[1])
        aw.set(model.get_weights())

        queue.task_done()

        if i % (100 * THREADS) == 0:
            model.save(FILENAME)

    for thread in thread_store:
        thread.join()

    model.save(FILENAME)
