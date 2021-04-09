from argparse import Action
from enum import Enum


class ArgsParseEnum(Enum):

    def __str__(self):
        return self.name

    @staticmethod
    def from_value(cls, value):
        try:
            return cls[value]
        except:
            raise ValueError(f'Error, does not compute {value} not a valid enum {cls} ')


class DepthSize(ArgsParseEnum):
    VERY_SMALL = (150, 200)
    SMALL = (200, 400)
    MEDIUM = (400, 600)
    LARGE = (600, 1000)
    VERY_LARGE = (1000, 1600)


class BranchingFactor(ArgsParseEnum):
    VERY_SMALL = (1, 3)
    SMALL = (2, 4)
    MEDIUM = (3, 5)
    LARGE = (4, 6)
    VERY_LARGE = (5, 7)


class SelectableEnumAction(Action):
    def __init__(self, *args, **kwargs):
        choices: [ArgsParseEnum] = kwargs.pop('choices', None)
        choices: list[ArgsParseEnum]

        if choices is None:
            raise ValueError('Choices must have something in it')

        kwargs.setdefault('choices', tuple(e.__str__() for e in choices))

        super(SelectableEnumAction, self).__init__(**kwargs)
        self._choices = choices

    def __call__(self, parser, namespace, values, option_string=None):
        chosen = [x for x in self._choices if x.__str__() == values]
        if len(chosen) > 1:
            print(chosen)
            raise ValueError('Only one option allowed')
        setattr(namespace, self.dest, chosen[0])
