"""
Contains functions that will handle different forms of parsing.
"""

import argparse
import logging
import pathlib
import sys

from pfts.util.logging import log_context

logger = logging.getLogger(__name__)


def parse_input(arg_list: list | None = None) -> argparse.Namespace:
    """Parses inputs from command line, and creates a namespace for them.

    :param arg_list: CMD-styled inputs of strings, defaults to sys.argv[1:]
    :type arg_list: list

    :return: Namespace that contains all parsed inputs for the given arguements
    :rtype: argparse.Namespace
    """
    if arg_list is None:
        arg_list = sys.argv[1:]

    parser = argparse.ArgumentParser(
        description="Parse inputs from Command Line."
    )

    # Enable dev mode for more robust logging
    parser.add_argument(
        "--dev", action="store_true", help="Enables developer mode."
    )
    parser.add_argument(
        "-v",
        "--vbump",
        nargs="?",  # 0/1 arguements
        const="patch",  # The default if there are 0 args
        help="Increase any portion of the version.",
    )

    parser.add_argument(
        "--disablecov",
        action="store_true",
        help="Disables coverage report generation.",
    )

    args = parser.parse_args(arg_list)

    logger.info(f"Args read in from CLI are: {args}")

    return args


@log_context
def parse_init_file(filepath: pathlib.Path) -> int:
    """Parse version information out from the given the __init__ file.

    :param filepath: The file that contains version information.
    :type filepath: pathlib.Path
    :return: Line index of version location. -1 if logging information missing.
    :rtype: int
    """

    index = -1

    try:
        with open(filepath, "r") as fin:
            for idx, line in enumerate(fin.readlines()):
                if "__version__" in line:
                    index = idx
                    break
    except FileNotFoundError:
        logging.error(f"Could not find version file at {filepath.resolve()}!")

    if index == -1:
        logger.warning("No version information found. Defaulting to 0.0.0")

    return index
