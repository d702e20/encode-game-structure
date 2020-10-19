import json
from enum import Enum
from pprint import pprint

DEBUG = True


def write_cgs(file, cgs):
    with open(file, 'w+') as o:
        o.writelines(json.dumps(cgs))


class CGS:
    def __init__(self, formula={}, player_count=0, labeling={}, transitions={}, moves={}):
        self.formula = formula
        self.game_struct = {"player_count": player_count,
                            "labeling": labeling,
                            "transitions": transitions,
                            "moves": moves}


class MexicanMoves(Enum):
    WAIT = 0
    LEFT = -1
    RIGHT = 1
    OTHER = 1  # think bout this


def kill_method(source, value, length):
    return (source + value) % length


def generate_mexican():
    i = 0
    length = 3
    out = []
    for p1_move in MexicanMoves:
        for p2_move in MexicanMoves:
            for p3_move in MexicanMoves:
                i += 1
                state = [1, 1, 1]

                # for each player, kill if not wait
                if p1_move != MexicanMoves.WAIT:
                    state[(kill_method(0, p1_move.value, length))] = 0
                if p2_move != MexicanMoves.WAIT:
                    state[(kill_method(1, p2_move.value, length))] = 0
                if p3_move != MexicanMoves.WAIT:
                    state[(kill_method(2, p3_move.value, length))] = 0

                if DEBUG:
                    print(f"({i:2}) moves: {p1_move.value:2}, {p2_move.value:2}, {p3_move.value:2}, state: {state}")

                out += [p1_move.value, p2_move.value, p3_move.value, state]

    return out


if __name__ == '__main__':
    test = [{0: [1, 2, 3],
             1: [4, 5, 6],
             2: [7, 8, 9]}]

    cgs = CGS()
    pprint(generate_mexican())
    write_cgs("test.json", test)
