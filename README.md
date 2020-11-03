# encode-game-structure

## move encoding
Internally the range [-1 .. 2] reflects [left, wait, right, other] moves.
When serialised [0 .. 2] reflects [wait, left/other, right], such that we obtain a range [0 .. n) of natural numbers where n are moves.
