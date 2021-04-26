from enum import IntEnum

import numpy as np
from utils.configuration import Config
from utils.utility_functions import write_json


class Enforce(IntEnum):
    enforce = 0
    despite = 1

    def __str__(self):
        return self.name


class TemporalOperator(IntEnum):
    next = 0
    eventually = 1
    invariant = 2
    until = 3

    def __str__(self):
        return self.name


def get_next(labels: list[int], total_states, states) -> (np.array, np.array):
    """
        Takes all labels, and a list of all states available, and all of the states that we should return a label
         list and a state list of accessible labels / states from this point.
         (small to-do, could be to also return what moves should be taken inorder for us to reach this,
            if we want to ensure a true state at a specific point in the model checker)
    """
    next_state = np.array([])
    labels_here = np.array([])
    for state in states:
        next_state = np.append(next_state, total_states[int(state)])
        labels_here = np.append(labels_here, labels[int(state)])
    return labels_here, next_state


def early_termination(config: Config,
                      labels: list[int],
                      predecessors_list: dict):
    """
        Creates only atl_formulas that we can guarantee will be able to "early_terminate".
    """
    initial_available_labels, initial_available_next_sates = get_next(labels, predecessors_list, [0])
    non_initial_labels = [x for x in range(0, 12) if x not in initial_available_labels]

    atl_queries = {}
    for index in range(config.amount_of_atl_formulas):
        for true_or_false in [True, False]:
            for k in Enforce:
                for o in [x for x in TemporalOperator
                          if x not in [TemporalOperator.eventually, TemporalOperator.until]
                          and (x != TemporalOperator.invariant or not true_or_false)]:
                    """
                        gets a list of all TemporalOperators. BUT only if this is not eventually or until and if its 
                        invariant, we should only use it in a False state.
                        
                        The reason for this is that this function returns only early_termination, and eventually and
                         until will always explore the whole state space. And invariant will only terminate early if 
                         we force it to use a label that we know is not valid at some point.     
                    """
                    name = f'{config.name}_early_termination_{k}_{o}_{index}'

                    atl_queries[name] = {
                        f'{k} {o}': {
                            'players': list(config.random.choices(
                                range(0, config.number_of_players),
                                k=config.random.randint(0, config.number_of_players))),
                            'formula': {
                                'proposition': config.random.choice(non_initial_labels)
                                if o == TemporalOperator.invariant
                                else config.random.choice(initial_available_labels)
                            }
                        }
                    }

    for key, value in atl_queries.items():
        write_json(config.output.parent.joinpath('atl').joinpath(key + '.json'), value)


def whole_state_space(config: Config,
                      labels: list[int],
                      predecessors_list: dict):
    """
        Creates only atl_formulas that we can guarantee to explore the whole state space.
    """
    initial_available_labels, initial_available_next_sates = labels[len(labels) - 1], predecessors_list.get(
        len(labels) - 1)
    non_initial_labels = [x for x in range(0, 12) if x not in initial_available_labels]
    atl_queries = {}
    for index in range(config.amount_of_atl_formulas):
        for true_or_false in [True, False]:
            for k in Enforce:
                for o in TemporalOperator:
                    pre = {}
                    until = {}
                    """
                    """
                    if o == TemporalOperator.until:
                        pre['pre'] = {
                            'proposition': 1 if true_or_false else 11
                        }
                        until['until'] = {
                            'proposition': 10
                        }
                    else:
                        pre['formula'] = {
                            'and': [
                                {'proposition': 10},
                                {'proposition': int(config.random.choices(initial_available_labels)[0])
                                if (k == Enforce.enforce and true_or_false) or
                                   (k == Enforce.despite and not true_or_false)
                                else int(config.random.choices(non_initial_labels)[0])}
                            ]
                        }
                    name = f'{config.name}_whole_statespace_{k}_{o}_{index}'
                    atl_queries[name] = {
                        f'{k} {o}': {
                            'players': list(range(0, config.number_of_players)),
                        }
                    }
                    atl_queries[name][f'{k} {o}'].update(pre)
                    if o == TemporalOperator.until:
                        atl_queries[name][f'{k} {o}'].update(until)

    for key, value in atl_queries.items():
        write_json(config.output.parent.joinpath('atl').joinpath(key + '.json'), value)


def complicated_formula():
    """
        Not implemented yet.
    """
    pass
