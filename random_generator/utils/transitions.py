import queue as python_queue
import random

from utils.configuration import Config
from utils.utility_functions import get_move_vector, get_resulting_states, mul


def transition_generator(config: Config):
    visited = set()
    depth = config.depth_size
    queue = python_queue.Queue()
    queue.put(0)
    visited.add(0)
    while not queue.empty():
        transitions_to: dict = {}
        q = queue.get()
        this_state_moves = [
            random.randint(1, config.max_num_moves)
            for _ in range(config.number_of_players)
        ]
        final_transitions = get_resulting_states(random, depth, mul(this_state_moves))
        for x in final_transitions:
            if transitions_to.get(q) is None:
                transitions_to[q] = []
            transitions_to[q].append(x)
            if x not in visited:
                visited.add(x)
                queue.put(x)

        true_labels_this_transition = [0] + ([1] if q > depth // 2 else []) + [i for i in range(2, 10) if config.random.randint(0, 5) != 0]

        yield true_labels_this_transition, \
              get_move_vector(this_state_moves, final_transitions), \
              this_state_moves, \
              transitions_to
