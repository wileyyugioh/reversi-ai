# wygameboard.py


empty = 0
black = 1
white = -1

class Board:
    """ Board for Reversii """
    class Error(RuntimeError):
        pass

    _init_board = [
                    empty, empty, empty, empty, empty, empty, empty, empty,
                    empty, empty, empty, empty, empty, empty, empty, empty,
                    empty, empty, empty, empty, empty, empty, empty, empty,
                    empty, empty, empty, white, black, empty, empty, empty,
                    empty, empty, empty, black, white, empty, empty, empty,
                    empty, empty, empty, empty, empty, empty, empty, empty,
                    empty, empty, empty, empty, empty, empty, empty, empty,
                    empty, empty, empty, empty, empty, empty, empty, empty,
                  ]

    def __init__(self, board=None):
        if not board:
            self._board = Board._init_board[:]
        else:
            self._board = board[:]

    def __str__(self):
        base = "    "
        for head in range(8):
            base += str(chr(65 + head)).rjust(4)
        base += "\n\n"
        for y in range(8):
            base += str(y + 1).rjust(3) + "  "
            for x in range(8):
                base += str(self._board[y * 8 + x]).rjust(3) + ","
            base += "\n"

        return base

    @staticmethod
    def move(positions):
        """ Create a move label """
        # Convert old coordinates into new
        leading = ord(positions[0]) - 65
        pos_init = 8 * (int(positions[1]) - 1) + leading

        return pos_init

    def get_state(self):
        """ Returns the board state """
        return self._board[:]

    def is_valid(self, pos, color):
        """ Returns True if the position is valid """
        X_MOVE = (-1, 0, 1)
        Y_MOVE = (-1, 0, 1)
        for x in X_MOVE:
            for y in Y_MOVE:
                curr_pos = pos
                moved = False
                while True:
                    new_pos = curr_pos + y * 8 + x

                    if(new_pos < 0 or new_pos > 63 or
                         abs(new_pos % 8 - curr_pos % 8) == 7):
                        break

                    status = self._board[new_pos]

                    if status == empty:
                        break

                    if status == color:
                        if moved:
                            return True
                        break

                    curr_pos = new_pos
                    moved = True
        return False

    def update(self, position, color):
        """ Update the board with new piece """
        if self._board[position] != empty:
            raise Board.Error("Invalid move")

        X_MOVE = (-1, 0, 1)
        Y_MOVE = (-1, 0, 1)

        valid = False
        for x in X_MOVE:
            for y in Y_MOVE:
                if x == 0 and y == 0:
                    continue
                found_sandwich = False
                curr_pos = position

                while True:
                    new_pos = curr_pos + y * 8 + x

                    if(new_pos < 0 or new_pos > 63 or
                       abs(new_pos % 8 - curr_pos % 8) == 7):
                        break

                    status = self._board[new_pos]

                    if status == empty:
                        break

                    if status is color:
                        found_sandwich = True
                        valid = True
                        break

                    curr_pos = new_pos

                # And we do it agian!
                while curr_pos != position and found_sandwich:
                    # Assumed that this means we found a sandwich
                    self._board[curr_pos] = color
                    curr_pos = curr_pos - y * 8 - x

        if not valid:
            raise Board.Error("Invalid move")

        # Add the added piece
        self._board[position] = color

    def score(self):
        """ Returns the score of the board """
        # [BLACK, WHITE]
        return [self._board.count(black), self._board.count(white)]

    def get_valid_moves(self, color):
        """ Returns a list of valid moves """
        moves = []
        for pos in range(len(self._board)):
            if self._board[pos] != empty:
                continue
            if self.is_valid(pos, color):
                moves.append(pos)
        return moves

    def has_valid_move(self, color):
        """ Returns True if a valid move is possible """
        for pos in range(len(self._board)):
            if self._board[pos] != empty:
                continue
            if self.is_valid(pos, color):
                return True
        return False


def main():
    b = Board()
    print(b.has_valid_move(black))
    print(b.has_valid_move(white))


if __name__ == "__main__":
    main()
