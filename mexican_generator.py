import json
from enum import Enum
from pprint import pprint
import collections.abc

DEBUG = True


def write_cgs(file, cgs):
    def set_default(obj):
        if isinstance(obj, set):
            return list(obj)
        raise TypeError

    with open(file, 'w+') as o:
        o.writelines(json.dumps(cgs, default=set_default))


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


def update(d, u):
    """
    https://stackoverflow.com/questions/3232943/update-value-of-a-nested-dictionary-of-varying-depth
    """
    for k, v in u.items():
        if isinstance(v, collections.abc.Mapping):
            d[k] = update(d.get(k, {}), v)
        else:
            d[k] = v
    return d


def generate_mexican(cgs: CGS):
    # transitions[state][player1choice][player2choice][player3choice] -> new_state
    i = 0
    length = 3
    out = []
    for state in range(0, 8):
        cgs.game_struct['transitions'].update({state: {}})

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

                out += [[p1_move.value, p2_move.value, p3_move.value, state]]
                print()
                entry = {p1_move.value: {p2_move.value: {p3_move.value: {''.join(map(str, state))}}}}
                cgs.game_struct['transitions'][7] = update(cgs.game_struct['transitions'][7], entry)

    return out


if __name__ == '__main__':
    test = [{0: [1, 2, 3],
             1: [4, 5, 6],
             2: [7, 8, 9]}]

    cgs = CGS(player_count=3)
    gen = generate_mexican(cgs)
    pprint(gen)

    pprint(cgs.game_struct)
    write_cgs("test.json", cgs.game_struct)
