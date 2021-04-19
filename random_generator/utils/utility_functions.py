import json
import operator
from pathlib import Path
from typing import Callable


def write_json(file: Path, json_obj):
    """Writes something of yupe JSON to a file"""
    file.parent.mkdir(parents=True, exist_ok=True)
    with open(file, 'w') as o:
        o.write(json.dumps(json_obj))


def reduce(function: Callable[[int, int], int], iterable: list[int]) -> int:
    """
        Reduces a function into a recursive call for calling all elements in a list to said function.
        In this example it is exclusively used with mul, and thus is used to multiply all numbers in a list
    """
    if len(iterable) == 1:
        return iterable[0]
    return function(iterable[0], reduce(function, iterable[1:]))


def mul(iterable: list[int]) -> int:
    """
        Calls reduce with a multiplication operator, on a list. Reduce makes sure that the multiplication operator is
         recursively called on all elements in a list.
        So with the input:
        [2, 5, 10]

        The result would be 2 * 5 * 10 = 100
    """
    return reduce(lambda x, y: operator.mul(x, y), iterable)


def get_resulting_states(random, max_trans: int) -> int:
    """
        For the total amount of moves that all players can take in our current state,
        this returns a random integer between 0 and the max amount of states.
        Resulting in a list that can with the chunk command be divided up to generate a move vector
    """
    return random.randint(0, max_trans - 1)


def chunks(li, n):
    """
        Pretty simple function. Takes a list, and a number of elements we want from said list.
        Then recursively calls itself and yields a nested list split into chunks of size n.

        Eg.
        chunks([1,2,3,4,5,6,7,8], 2)
        -> [[1,2],[3,4],[5,6],[7,8]]
    """
    if not li:
        return
    yield li[:n]
    yield from chunks(li[n:], n)


def get_move_vector(player_moves: list[int], list_of_final_transitions: list[int]):
    """
        This is where the move vector is created. By using recursive calls and making sure that all players have the
        amount of moves specified in the list player_moves.

        Eg.
        get_move_vector([2,2,2], [1,2,3,4,5,6,7,8])
        -> [[[1, 2], [3, 4]], [[5, 6], [7, 8]]]
    """
    res: list = []
    move_chunks = chunks(list_of_final_transitions, int(len(list_of_final_transitions) / player_moves[0]))
    if len(player_moves) > 2:
        for chunk in move_chunks:
            res.append([x for x in get_move_vector(player_moves[1:], chunk)])
    elif len(player_moves) == 2:
        [res.append(chunk) for chunk in move_chunks]
    return res
