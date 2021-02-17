from utils.conversions import all_states


class CGS:

    def __init__(self, player_count=0):
        self.game_struct = {"player_count": player_count,
                            "labeling": [],
                            "transitions": [[] for _ in all_states()],
                            "moves": []}

    def add_trans(self, q, move, result_state):
        # shifting up by once so moves are in range {0, 1, 2} and mapping 'other' to 'right' (convert to list for edit)
        move = list(move)

        # not very pretty, but works for mapping [-1 .. 2] to [0 .. n)
        for i, m in enumerate(move):
            if m == -1:
                move[i] = 0
            if m == 0:
                move[i] = -1
            if m == 1:  # for completeness
                move[i] = 1
            if m == 2:
                move[i] = 0

        entry = [move[0] + 1, [move[1] + 1, [move[2] + 1, [result_state]]]]
        self.game_struct['transitions'][q].append(entry)

    def append_label(self, labels):
        self.game_struct['labeling'].append(labels)

    def append_move(self, moves):
        self.game_struct['moves'].append(moves)
