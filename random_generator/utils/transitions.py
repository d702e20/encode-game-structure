import queue as python_queue
import random

from utils.configuration import Config
from utils.utility_functions import get_player_chunk, get_x_final_transitions, mul


def transition_generator(config: Config):
    visited = set()
    depth = config.random.randint(*config.depth.value)
    queue = python_queue.Queue()
    queue.put(0)
    visited.add(0)
    while not queue.empty():
        q = queue.get()
        if q + 1 < depth and (q + 1) not in visited:
            config.logger.debug(q + 1)
            visited.add(q + 1)
            queue.put(q + 1)
        this_state_moves = [
            random.randint(1, config.max_num_moves)
            for _ in range(config.number_of_players)
        ]
        yield get_player_chunk(this_state_moves,
                               get_x_final_transitions(random, depth, mul(this_state_moves))), this_state_moves
