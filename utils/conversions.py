from typing import Union
import collections.abc


def get_binary_rep(val: int) -> str:
    return format(val, 'b')


def get_base10_rep_from_binary_array(val: [int]):
    return get_base10_rep(str(''.join(map(str, val))))


def all_states():
    return [state for state in range(0, 8)]


def get_base10_rep(val: Union[int, str]) -> int:
    return int(str(val), 2)


def update(d, u):
    """
    https://stackoverflow.com/questions/3232943/update-value-of-a-nested-dictionary-of-varying-depth
    """
    for k, v in u.items():
        if isinstance(v, collections.abc.Mapping):
            d[k] = update(d.get(k, {}), v)
        else:
            d[k] = v
    return d



