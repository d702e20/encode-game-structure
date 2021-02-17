import unittest

from generators.MexicanGenerators import *


class KillTests(unittest.TestCase):

    def test_result(self):
        length = 3

        # killing right from end should give 0
        self.assertEqual(0, kill_method(2, 1, length))

        # killing left from start should give length -1
        self.assertEqual(length - 1, kill_method(0, -1, length))

        # killing right from length - 2 should give source + 1
        self.assertEqual(2, kill_method(1, 1, length))


class ValidTests(unittest.TestCase):

    def test_valid_positive(self):
        def valid_pos(source, target, move):
            self.assertEqual(target, move_valid(source, move).base10_rep())

        # three players
        # q111 given [0,0,0] should give q111 -> wait
        valid_pos(7, 7, [0, 0, 0])

        # q111 given [1,0,0] should give q101 -> two players
        valid_pos(7, 5, [1, 0, 0])

        # q111 given [1,0,0] should give q100 -> one player
        valid_pos(7, 4, [1, 1, 0])

        # two players
        # q110 given [0, 2, 0] should give q010
        valid_pos(6, 2, [0, 2, 0])

        # q101 given [2, 0, 0] should give q100
        valid_pos(5, 4, [2, 0, 0])

        # q011 given [0, 2, 0] should give q010
        valid_pos(3, 2, [0, 2, 0])

        # one player
        # q100 given [0, 0, 0] should give q100
        valid_pos(4, 4, [0, 0, 0])

    def test_valid_negative(self):
        def valid_neg(source, move):
            self.assertFalse(move_valid(source, move))

        # give illegal move vectors and assert false
        # three players
        valid_neg(7, [2, 0, 0])

        valid_neg(7, [0, 2, 0])

        valid_neg(7, [1, 0, 2])

        # two players
        valid_neg(6, [0, 1, 1])

        valid_neg(5, [1, 0, 0])

        valid_neg(3, [0, -1, 0])

        # one player
        valid_neg(4, [1, 0, 0])


if __name__ == '__main__':
    unittest.main()
