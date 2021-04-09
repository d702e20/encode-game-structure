import pathlib

from utils.atl_functions import early_termination, whole_state_space
from utils.transitions import transition_generator
from utils.configuration import get_config
from utils.utility_functions import write_json

config = get_config(pathlib.Path(__file__).parent)

transitions = transition_generator(config)
result = {
    'player_count': config.number_of_players,
    'labeling': [],
    'transitions': [],
    'moves': []
}

predecessors_list: dict = {}

vv = set()
config.logger.info(config.__str__())
whoop = config.depth_size
while True:
    try:
        whoop -= 1
        transition = next(transitions)
        result['labeling'].append(transition[0])
        result['transitions'].append(transition[1])
        result['moves'].append(transition[2])
        config.logger.info(f'Countdown: {whoop}')
        for key, value in transition[3].items():
            if predecessors_list.get(key) is None:
                predecessors_list[key] = value
            else:
                [predecessors_list[key].add(x) for x in value]
    except StopIteration:
        result['labeling'][-1].append(10)
        result['labeling'][0].append(11)
        break
config.logger.info('done')

config.logger.debug('Starting early_termination_generation')
early_termination(config, result['labeling'], predecessors_list)
config.logger.debug('done')

config.logger.debug('Starting whole_statespace_termination_generation')
whole_state_space(config, result['labeling'], predecessors_list)
config.logger.debug('done')

config.logger.debug('Writing cgs to file')
write_json(config.output, result)
config.logger.debug('done')
