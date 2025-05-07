"""Contains general utility functions."""

import logging.config
import pathlib

import pfts
from pfts.util import parsing
from pfts.util.logging import log_context

logger = logging.getLogger(__name__)


@log_context
def return_true() -> bool:
    """
    Allows for testing that every imports as expected.

    :return: Will always return True
    :rtype: bool
    """
    return True


@log_context
def bump_version(part: str, testing_mode: bool = False) -> str:
    """Increments either the major, minor, or patch version of the pfts module.

    :param part: Which part of the version to increment.
    :type part: str
    :param testing_mode: Whether to run in debug mode or not, defaults to False
    :type testing_mode: bool, optional
    :return: If debugging, return new version info. Otherwise return nothing.
    :rtype: str|None
    """
    part = part.lower()
    if part not in ["major", "minor", "patch"]:
        version = pfts.__version__
        logger.error(f"Unknown part: {part}. Version is still: {version}")
        return version

    real_init = pathlib.Path("pfts") / "__init__.py"
    mock_init = pathlib.Path("tests/data/mock_init.txt")

    version_file = real_init if not testing_mode else mock_init

    # Will only change __version__ information of the file.
    # Everything else will stay the same in the same order.
    # Parsing file is to ensure that __version__ can be anywhere in the file
    version_index = parsing.parse_init_file(version_file)

    # If something went wrong with the parsing, default the version
    if version_index == -1:
        file_information = []
        version_info = "__version__ = '0.0.0'"
    else:
        with open(version_file, "r") as fin:
            file_information = fin.readlines()

            # ___version__ = 'x.x.x' <- Line format
            version_info = file_information[version_index]

    v_dict = split_version_line(version_info)
    v_dict[part] += 1

    new_version = f"{v_dict['major']}.{v_dict['minor']}.{v_dict['patch']}"

    new_line = f"__version__ = '{new_version}'\n"

    logger.info(
        f"Old version: {version_info.strip()}; "
        f"New_Version: {new_version.strip()}"
    )

    insert_into_file(version_file, new_line, file_information, version_index)

    return new_version


@log_context
def split_version_line(version: str) -> dict[str, int]:
    """Takes in a version declaration, creates dict of version information.

    __version__ = 'X.Y.Z' → {major: X, minor: Y, patch: Z}

    :param version: Line containing the version definition.
    :type version: str
    :return: Version dictionary split by major, minor and patch parts.
    :rtype: dict[str, int]
    """
    major, minor, patch = [
        int(x)
        for x in version.split("=")[1].strip().strip('"').strip("'").split(".")
    ]

    v_dict = {"major": major, "minor": minor, "patch": patch}

    return v_dict


@log_context
def insert_into_file(
    filepath: pathlib.Path,
    insert_portion: str,
    rest_of_file: list[str],
    insert_index: int,
) -> None:
    """Take a line and insert it into a file.

    :param filepath: Location of the file to work with.
    :type filepath: pathlib.Path
    :param insert_portion: The line being inserted.
    :type insert_portion: str
    :param rest_of_files: The rest of the file, in order.
    :type rest_of_files: list[str]
    :param insert_index: Where to insert the new line.
    :type insert_index: int
    """

    if not rest_of_file:
        rest_of_file = [insert_portion]
    else:
        rest_of_file[insert_index] = insert_portion

    with open(filepath, "w") as fout:
        fout.writelines(rest_of_file)
