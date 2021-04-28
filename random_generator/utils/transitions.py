import queue as python_queue
import random

from utils.configuration import Config
from utils.utility_functions import get_move_vector, get_resulting_states, mul


def transition_generator(config: Config):
    visited = set()
    depth = config.depth_size
    for current_index in range(config.depth_size):
        transitions_to: dict = {}
        this_state_moves = [
            random.randint(1, config.max_num_moves)
            for _ in range(config.number_of_players)
        ]
        final_transitions = []
        for _ in range(mul(this_state_moves)):
            x = get_resulting_states(random, depth)
            final_transitions.append(x)
            if transitions_to.get(current_index) is None:
                transitions_to[current_index] = []
            transitions_to[current_index].append(x)

        true_labels_this_transition = [0] + ([1] if current_index > depth // 2 else []) + [i for i in range(2, 10) if config.random.randint(0, 5) != 0]

        yield true_labels_this_transition, \
              final_transitions if len(final_transitions) == 1 else get_move_vector(this_state_moves, final_transitions), \
              this_state_moves, \
              transitions_to
