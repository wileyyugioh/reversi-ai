# wyeval_single.py

import numpy as np
from keras.models import load_model


class Team:
    EMPTY = 0
    WHITE = -1
    BLACK = 1


class Coordinate:
    """ Represents tensorflow coordinates and normal """
    def Error(ValueError):
        pass

    def __init__(self, x, y=None):
        if y:
            if not(0 <= x <= 7 and 0 <= y <= 7):
                raise Coordinate.Error("Invalid coordinate {}, {}".format(x, y))
            self._x = x
            self._y = y
            self._n = x * 8 + y
        else:
            if not(0 <= x <= 63):
                raise Coordinate.Error("Invalid coordinate {}".format(x))

            self._x = x % 8
            self._y = x // 8
            self._n = x

    def get(self):
        """ Get the coordinate as (x, y) """
        return self._x, self._y

    def get_flat(self):
        """ Get the coordinate as N """
        return self._n

    def __str__(self):
        coord_format = chr(self._x + 65) + str(self._y + 1)
        return "{} ({},{})".format(coord_format, self._x, self._y)

    def __lt__(self, that):
        return self._n < that._n


class Board:
    """ Converts game board list to numpy """
    class Error(TypeError):
        pass

    def __init__(self, data, color):

        if not(isinstance(data, list) and -1 <= color <= 1):
            raise Board.Error("Invalid type passed in")

        self._color = np.array([color])
        self._data = np.array(data, ndmin=2)
        if isinstance(data[0], list):
            # 2D List
            self._data = self._data.flatten()

    def data(self):
        """ Returns the numpy game board and color """
        return [self._data, self._color]


class ModelPredictor:
    """ Loads a created model and predicts the next move """
    def __init__(self, filename="reversi3.h5"):
        self._model = load_model(filename)


    @staticmethod
    def _valid_predict(board, data, color, coord):
        """ Returns True if the coordinate is valid """
        return (data[coord] == Team.EMPTY and
                board.is_valid(coord, color))

    def _do_predict(self, data, color):
        """ Return raw predictions """
        board = Board(data, color)
        input_data = board.data()

        predict_results = self._model.predict(input_data)

        generate = [[Coordinate(i), prob] for i, prob in enumerate(predict_results[0])]
        if color == Team.BLACK:
            generate.sort(key=lambda tup: tup[1], reverse=True)
        else:
            generate.sort(key=lambda tup: tup[1])
        return generate

    def predict(self, board, color):
        """ Return best valid prediction """
        data = board.get_state()
        raw_predicts = self._do_predict(data, color)

        for single in raw_predicts:
            if ModelPredictor._valid_predict(board, data, color, single[0].get_flat()):
                return single[0]


def main(run_times):
    import wygameboard

    mp = ModelPredictor()
    for _ in range(run_times):
        gb = wygameboard.Board()
        color = Team.BLACK
        while True:
            # Predict moves
            if times == 1:
                print(gb)
            prediction = mp.predict(gb, color)
            if prediction:
                gb.update(prediction.get_flat(), color)

            if gb.has_valid_move(-color):
                color = -color
            elif gb.has_valid_move(color):
                if times == 1:
                    print("PASSING {}".format(-color))
            else:
                break
        print(gb.score())

if __name__ == "__main__":
    import sys
    args = sys.argv
    try:
        times = int(sys.argv[1])
    except:
        times = 1
    main(times)
