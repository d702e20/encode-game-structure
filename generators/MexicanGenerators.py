import queue as python_queue
import copy
from enum import IntEnum
from pprint import pprint

from domain.CGS import CGS
from domain.CGSGenerator import CGSGenerator
from domain.State import State
from utils.conversions import get_base10_rep_from_binary_array
from utils.io import write_cgs

DEBUG = False
USE_LISTS = True  # if false, uses dicts


class MexicanGenerator(CGSGenerator):

    def __init__(self):
        CGSGenerator.__init__(self)



class MexicanMoves(IntEnum):
    WAIT = 0
    LEFT = -1
    RIGHT = 1
    OTHER = 2


def kill_method(source, value, length):
    return (source + value) % length


def all_moves():
    ret = set()
    [[[ret.add((p1_move, p2_move, p3_move))
       for p1_move in MexicanMoves]
      for p2_move in MexicanMoves]
     for p3_move in MexicanMoves]
    return sorted(ret)


def all_states():
    return [state for state in range(0, 8)]


def move_valid(q, move):
    init_state = State(q)
    state = copy.deepcopy(init_state)
    length = 3
    assert init_state == state

    if DEBUG:
        print("Move valid computation:")

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
                    else:  # kill target (oi mate, u got a loicense t' kill?)
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
                # find index of other player
                for j in range(0, 3):
                    index = kill_method(i, j, length)
                    if init_state.state[index] != 1 or index == i:
                        continue
                    assert index != i  # no suicide please
                    assert state.state[index] == 1  # cannot kill dead people
                    # kill other player
                    state.state[index] = 0

    if alive_players == 1 or alive_players == 0:
        # if only one player, they can only wait
        for m in move:
            if m != 0:
                return False

    if DEBUG:
        print(f"resulting state: {state.state}")
    return state


def generate_mexican(cgs: CGS):
    queue = python_queue.Queue()
    queue.put(7)  # initialise with state q111 = 7
    visited = set()
    while not queue.empty():
        if DEBUG:
            print("\n==== NEW ITERATION ====")
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
                queue.put(target_state)

            # add current state to visited
            visited.add(target_state)


def generate_labeling(cgs: CGS):
    for n in all_states():
        state = State(n)
        res = []
        for i, alive in enumerate(state.state):
            if alive:
                res.append(i + 1)
        cgs.append_label(res)




if __name__ == '__main__':
    cgs = CGS(player_count=3)

    # generate \pi
    generate_labeling(cgs)  # fixme: dict with state instead of inferring state based on array position?

    # generate transition function
    generate_mexican(cgs)

    # hotfix for fixing duplicates for list output
    if USE_LISTS:
        cgs.game_struct['transitions'][7] = cgs.game_struct['transitions'][7][:27]

    # generate number of moves per state
    generate_num_moves(cgs)  # fixme: dict with state instead of inferring state based on array position?

    pprint(cgs.game_struct)
    write_cgs(f"mexican-standoff-{'list' if USE_LISTS else 'dict'}.json", cgs.game_struct)
