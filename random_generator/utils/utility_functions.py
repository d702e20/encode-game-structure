import json
import operator
from pathlib import Path
from typing import Callable


def write_json(file: Path, json_obj):
    file.parent.mkdir(parents=True, exist_ok=True)
    with open(file, 'w') as o:
        o.write(json.dumps(json_obj))


def reduce(function: Callable[[int, int], int], iterable: list[int]) -> int:
    if len(iterable) == 1:
        return iterable[0]
    return function(iterable[0], reduce(function, iterable[1:]))


def mul(iterable: list[int]) -> int:
    return reduce(lambda x, y: operator.mul(x, y), iterable)


def get_x_final_transitions(random, max_trans: int, total_moves: int) -> list[int]:
    return [random.randint(0, max_trans - 1) for _ in range(total_moves)]


def chunks(li, n):
    if not li:
        return
    yield li[:n]
    yield from chunks(li[n:], n)


def get_move_vector(player_moves: list[int], list_of_final_transitions: list[int]):
    res: list = []
    move_chunks = chunks(list_of_final_transitions, int(len(list_of_final_transitions) / player_moves[0]))
    if len(player_moves) > 2:
        for chunk in move_chunks:
            res.append([x for x in get_move_vector(player_moves[1:], chunk)])
    elif len(player_moves) == 2:
        [res.append(chunk) for chunk in move_chunks]
    return res
