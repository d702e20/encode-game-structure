import json
import queue as python_queue
import copy
from enum import IntEnum
from pprint import pprint
import collections.abc
from typing import Union

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

    def add_trans(self, q, move, result_state):
        entry = {move[0]: {move[1]: {move[2]: {result_state}}}}  # resulting state as list?
        try:
            self.game_struct['transitions'][q]
        except KeyError:  # maybe q doesn't exist
            self.game_struct['transitions'].update({q: {}})
        finally:
            self.game_struct['transitions'][q] = update(self.game_struct['transitions'][q], entry)


class MexicanMoves(IntEnum):
    WAIT = 0
    LEFT = -1
    RIGHT = 1
    OTHER = 2  # think bout this


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


class State:
    def __init__(self, state_int):
        # Unroll base 10 rep to binary rep with leading zeroes
        bin_rep = list(map(int, get_binary_rep(state_int)))
        if len(bin_rep) == 1:
            bin_rep = [0] + bin_rep

        if len(bin_rep) == 2:
            bin_rep = [0] + bin_rep

        self.state = bin_rep

    def __eq__(self, other):
        return self.state == other.state

    def __str__(self):
        return str(self.state)

    def base10_rep(self):
        return get_base10_rep(self.__str__())


def all_moves():
    ret = set()
    [[[ret.add((p1_move, p2_move, p3_move))
       for p1_move in MexicanMoves]
      for p2_move in MexicanMoves]
     for p3_move in MexicanMoves]
    return sorted(ret)


def all_states():
    return [state for state in range(0, 8)]


def get_binary_rep(val: int) -> str:
    return format(val, 'b')


def get_base10_rep(val: Union[int, str]) -> int:
    return int(str(val), 2)


def get_base10_rep_from_binary_array(val: [int]):
    return get_base10_rep(str(''.join(map(str, val))))


def move_valid(q, move):
    init_state = State(q)
    state = copy.deepcopy(init_state)
    length = 3
    assert init_state == state

    # three player
    if DEBUG:
        print("Move valid:")

    # count alive players
    alive_players = init_state.state.count(1)

    if alive_players == 3:
        for i, m in enumerate(move):
            if DEBUG:
                print(f"i: {i}, m: {m}")

            # other in 3-player game is illegal
            if m == 2:
                return False

            # if dead, must wait:
            if init_state.state[i] == 0:
                if m != MexicanMoves.WAIT:
                    return False

            # else player is alive
            else:
                # if player wants to kill, target must initially have been alive
                if m != MexicanMoves.WAIT:
                    target = kill_method(i, m, length)
                    if init_state.state[target] == 0:
                        return False
                    else:  # kill target (the name's band, jahn band)
                        state.state[target] = 0

    if alive_players == 2:
        # only other or wait is allowed for non 3-player games
        for m in move:
            if not (m == 0 or m == 2):
                return False

        # look for Other, and kill other player if present, break on wait
        for i, m in enumerate(move):

            # if dead, must wait:
            if init_state.state[i] == 0:
                if m != MexicanMoves.WAIT:
                    return False

            # player i chose to kill other
            if m == 2:
                # find index of other player, this works because only two are present and we start searching after p_i
                for j in range(1, 3):  # TODO
                    if init_state.state[(i + j) % length] != 1:
                        continue
                    # kill other player
                    state.state[j] = 0
                    break  # good measure

    if alive_players == 1 or alive_players == 0:
        # if only one player, they can only wait
        for m in move:
            if m != 0:
                return False

    if DEBUG:
        print(f"resulting state: {state.state}")
    return state

    """
    for each part of move
        check if legal,
        then execute
        
        a player can shoot a dead player only if that player was a live to begin with
        
    check if in 3 player mode or 2 player mode (or 1 player mode)
    
    use kill_method to get player who dies
    """


def generate_mexican(cgs: CGS):
    queue = python_queue.Queue()
    # [queue.put(state) for state in all_states()]
    queue.put(7)  # initialise with state q111 = 7
    visited = set()
    while not queue.empty():
        print("\n==== NEW ITER ====")
        # pop a state off the queue to explore
        q = queue.get()
        for move in all_moves():
            # ignore moves which are not valid
            if DEBUG:
                print(f"q: {q}, move: {[m.value for m in move]}")
            result_state = move_valid(q, move)
            if not result_state:
                if DEBUG:
                    print("Move invalid")
                continue

            # convert resulting state to base10
            target_state = get_base10_rep_from_binary_array(result_state.state)

            # add valid transaction to cgs transitions
            cgs.add_trans(q, move, target_state)

            # add any state targets found to queue
            if target_state not in visited:
                queue.put(target_state)  # move_target(q, move)

            # add current state to visited
            visited.add(target_state)


if __name__ == '__main__':
    # transitions[state][player1choice][player2choice][player3choice] -> new_state
    cgs = CGS(player_count=3)

    generate_mexican(cgs)
    pprint(cgs.game_struct)

    write_cgs("test.json", cgs.game_struct)
