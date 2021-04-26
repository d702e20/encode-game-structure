from enum import IntEnum
from logging import CRITICAL, FATAL, ERROR, WARNING, WARN, INFO, DEBUG


class VerbosityOptions(IntEnum):
    """Verbosity options for logger in the configuration."""

    CRITICAL = CRITICAL
    FATAL = FATAL
    ERROR = ERROR
    WARNING = WARNING
    WARN = WARN
    INFO = INFO
    DEBUG = DEBUG

    def __str__(self):
        return self.name

    @staticmethod
    def verbose_type(s):
        try:
            return VerbosityOptions[s]
        except KeyError:
            raise ValueError()
