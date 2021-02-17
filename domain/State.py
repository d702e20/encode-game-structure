from utils.conversions import get_base10_rep_from_binary_array, get_binary_rep


class State:
    def __init__(self, state_int):
        # Unroll base 10 rep to binary rep with leading zeroes
        bin_rep = list(map(int, get_binary_rep(state_int)))
        if len(bin_rep) == 1:
            bin_rep = [0] + bin_rep

        if len(bin_rep) == 2:
            bin_rep = [0] + bin_rep

        self.state = bin_rep

    def __eq__(self, other):
        return self.state == other.state

    def __str__(self):
        return str(self.state)

    def base10_rep(self):
        return get_base10_rep_from_binary_array(self.state)

