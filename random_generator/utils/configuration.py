import argparse
import json
import time
from pathlib import Path
import logging
import random as python_random

from . import SelectableEnumAction, DepthSize, BranchingFactor


class Config:
    seed: any = ''
    output: Path
    config_out: Path
    depth: DepthSize
    branching: BranchingFactor
    logger: logging.Logger
    random: python_random
    number_of_players: int
    max_num_moves: int

    def __init__(self, initial_config: dict):
        if initial_config['config'] is not None:
            self.__read_config(initial_config['config'])
        else:
            self.__set_config(initial_config)

    def __set_config(self, config: dict):

        if config['seed'] is not None:
            self.seed += config['seed']

        if config['very_random_generator']:
            self.seed += time.time()

        self.output = config['output']
        self.config_out = config['config_out']
        self.depth = config['depth']
        self.branching = config['branching']
        self.logger = config['logger']
        self.random = python_random
        self.random.seed(self.seed)
        self.number_of_players = self.random.randint(*self.branching.value)
        self.max_num_moves = self.random.randint(*self.branching.value)

    def __read_config(self, config_location: str):
        with open(config_location, 'r+') as f:
            obj = json.load(f)
            self.__set_config(obj)
            self.number_of_players = obj['number_of_players']
            self.max_num_moves = obj['max_num_moves']

    def __dict__(self):
        return {
            'seed': self.seed,
            'depth': self.depth,
            'branching': self.branching,
            'number_of_players': self.number_of_players,
            'max_num_moves': self.max_num_moves
        }

    def __str__(self):
        return "(" + "".join(["{'" + str(key) + "': '" + str(value) + "'}, {" for key, value in self.__dict__().items()]) + ")"

    def write_config(self):
        self.output.parent.mkdir(parents=True)
        with open(self.output, 'w+') as f:
            f.write(json.dumps(self.__dict__))
        return self


def get_config(root_dir: Path):
    args = argparse.ArgumentParser()
    default_config_place = root_dir.joinpath('config').joinpath('config.json')
    args.add_argument('-c', '--config', default=None, help='config figuration in json format')
    args.add_argument('--config-out', default=default_config_place, help='Output of the configuration file')
    args.add_argument('-o', '--output', default=root_dir.joinpath('output').joinpath('random.json'),
                      help='output of the randomCGS')

    settings_args = args.add_argument_group(title='randomizer settings')
    settings_args.add_argument('--very-random-generator', action='store_true',
                               required=False, default=False, help='If enabled, will use timestamp in addition '
                                                    'to seed to provide a "very random_generator" experience')
    settings_args.add_argument('-d', '--depth', action=SelectableEnumAction, choices=DepthSize,
                               default=DepthSize.MEDIUM, help='Depth size')

    settings_args.add_argument('-b', '--branching', action=SelectableEnumAction, choices=BranchingFactor,
                               default=BranchingFactor.MEDIUM, help='Branching factor')
    settings_args.add_argument('-s', '--seed', default=None,
                               help='Default: None.')

    cc = args.parse_args().__dict__
    cc['root'] = root_dir
    cc['name'] = cc['output'].name
    logger = logging.getLogger('random-generator')

    cc['logger'] = logging.getLogger('random-generator')
    cc['logger']: logging.Logger

    return Config(cc)
