from enum import IntEnum
import logging

from domain.CGS import CGS
from domain.State import State


class CGSGenerator:
    cgs: CGS = None
    moves: IntEnum
    logger: logging.Logger

    def __init__(self):
        self.logger = logging.getLogger(self.__name__)
        self.cgs = CGS()

    def set_cgs(self, cgs: CGS):
        self.cgs = cgs

    def generate_states(self, num_states: list[int]):
        self.__generate_num_moves(self.cgs, num_states)

    def update_function(self):
        raise NotImplemented()

    def set_moves(self, moves: IntEnum):
        self.moves = moves

    def generate_labels(self):
        pass

    def generate_players(self):
        pass

    def generate_number_of_moves(self):
        pass

    def __write_cgs(self):
        pass

    def __generate_num_moves(self, cgs: CGS, num_states: [int]):
        n: int
        for n in num_states():
            state = State(n)
            alive_players = state.state.count(1)
            res = []
            for i, alive in enumerate(state.state):
                res.append(alive_players if alive else 1)
            cgs.append_move(res)
