import pathlib

from utils.transitions import transition_generator
from utils.configuration import get_config
from utils.utility_functions import write_cgs

config = get_config(pathlib.Path(__file__).parent)

transitions = transition_generator(config)
result = {
    'player_count': config.number_of_players,
    'labeling': [],
    'transitions': [],
    'moves': []
}
while True:
    try:
        transition = next(transitions)
        result['labeling'].append([i for i in range(0, 10) if config.random.randint(0, 5) != 0])
        result['transitions'].append(transition[0])
        result['moves'].append(transition[1])
    except StopIteration:
        break
write_cgs(config.output, result)
