# wytest.py

from wyeval_single import ModelPredictor
from wygameboard import Board


def run_bot(mp, gb, color):
    """ Run the bot prediction code and update board """
    nxt = mp.predict(gb, color)
    gb.update(nxt.get_flat(), color)
    print(gb)
    print(nxt)


def run_human(gb, color):
    """ Get human input and update board """
    while True:
        try:
            human_in = input("Where do you place piece? (ex. A4) ").upper()
            flat_coord = gb.move(human_in)
            gb.update(flat_coord, color)
        except IndexError as e:
            raise e
        else:
            break


def main():
    gb = Board()
    mp = ModelPredictor()
    while True:
        is_first = int(input("Is bot first? (1 yes, 0 no) "))
        if is_first == 0 or is_first == 1:
            break

    if not is_first:
        bot_color = -1
        human_color = 1
        curr_color = human_color

    else:
        bot_color = 1
        human_color = -1
        curr_color = bot_color

    while True:
        if curr_color == bot_color:
            run_bot(mp, gb, bot_color)
        else:
            try:
                run_human(gb, human_color)
            except Board.Error:
                continue

        if gb.has_valid_move(-curr_color):
            curr_color = -curr_color
        elif gb.has_valid_move(curr_color):
            print("SKIPPING {}".format(-curr_color))
        else:
            print("GAME END")
            break

    print(gb.score())


main()
