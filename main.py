import logging
import argparse

from utils.VerbosityOptions import VerbosityOptions

args = argparse.ArgumentParser()
args.add_argument("-v", default=VerbosityOptions.INFO, required=False, type=VerbosityOptions.verbose_type,
                  choices=list(VerbosityOptions),
                  help="Give one of the options to determine how verbose that you want the logging to be")


parsed_args = args.parse_args()


def main():
    logging.basicConfig(level=parsed_args.v)


if __name__ == '__main__':
    pass
    main()
