# encode-game-structure

## move encoding
Internally the range [-1 .. 2] reflects [left, wait, right, other] moves.
When serialised [0 .. 2] reflects [wait, left/other, right], such that we obtain a range [0 .. n) of natural numbers where n are moves.


## Random generator

Run this as `python random_generator` as this is created as a python module.

### Help
```
usage: random_generator [-h] [-c CONFIG] [--config-out CONFIG_OUT] [-o OUTPUT] [--very-random-generator]
                        [-d {VERY_SMALL,SMALL,MEDIUM,LARGE,VERY_LARGE}]
                        [-b {VERY_SMALL,SMALL,MEDIUM,LARGE,VERY_LARGE}] [-s SEED]

optional arguments:
  -h, --help            show this help message and exit
  -c CONFIG, --config CONFIG
                        config figuration in json format
  --config-out CONFIG_OUT
                        Output of the configuration file
  -o OUTPUT, --output OUTPUT
                        output of the randomCGS

randomizer settings:
  --very-random-generator
                        If enabled, will use timestamp in addition to seed to provide a "very
                        random_generator" experience
  -d {VERY_SMALL,SMALL,MEDIUM,LARGE,VERY_LARGE}, --depth {VERY_SMALL,SMALL,MEDIUM,LARGE,VERY_LARGE}
                        Depth size
  -b {VERY_SMALL,SMALL,MEDIUM,LARGE,VERY_LARGE}, --branching {VERY_SMALL,SMALL,MEDIUM,LARGE,VERY_LARGE}
                        Branching factor
  -s SEED, --seed SEED  Default: None.
```
