"""
Describes the different entry points for this tool.
"""

import logging
import os
import pathlib
import subprocess  # nosec B404
import webbrowser

from pfts.util import general
from pfts.util.logging import process_logging, setup_logging
from pfts.util.parsing import parse_input

logger = logging.getLogger(__name__)


def generate_documentation() -> None:
    """Generate documentation for the current codebase and opens it."""
    setup_logging()
    logger = logging.getLogger(__name__)

    orig_cwd = pathlib.Path().cwd()

    # Ensure that we are in docs folder for Sphinx
    docs_folder = orig_cwd / "docs"
    os.chdir(docs_folder)
    make_location = str(pathlib.Path("./make.bat").resolve())

    gen_args = ["sphinx-apidoc", "-o", "./source", "../pfts"]

    # Create the .rst files for Sphinx
    generation_process_rtncode = subprocess.call(
        gen_args,
        stdout=subprocess.DEVNULL,
    )  # nosec B603

    process_logging(logger, generation_process_rtncode, "Sphinx-API")

    make_clean_args = [make_location, "clean"]
    make_run_args = [make_location, "html"]

    logger.info("Removing all existing docs under build.")
    # Remove any previous documents just in case
    subprocess.call(make_clean_args, stdout=subprocess.DEVNULL)  # nosec B603

    make_rtncode = subprocess.call(make_run_args, stdout=subprocess.DEVNULL)  # nosec B603

    process_logging(logger, make_rtncode, "Make Process")

    doc_file_str = str(pathlib.Path("./build/html/index.html").resolve())
    logger.info(f"Documentation created at: {doc_file_str}")
    webbrowser.open(doc_file_str, 1)

    os.chdir(orig_cwd)


def run_testing(arg_list: list | None = None) -> None:
    """Run the entire test suite, and potentially generate a coverage file.

    :param arg_list: CLI Interface, defaults to None
    :type arg_list: list | None
    """

    args = parse_input(arg_list)

    coverage_args = ["coverage", "run", "-m", "pytest"]
    # Not generating logs since pytest will take over the logging.
    subprocess.call(coverage_args)  # nosec B603

    if not args.disablecov:
        report_gen_args = ["coverage", "html", "-d", "coverage_report"]
        subprocess.call(report_gen_args)  # nosec B603

        coverage_filepath = str(
            pathlib.Path().cwd() / "coverage_report" / "index.html"
        )
        webbrowser.open(coverage_filepath, 1)


def run_local_ci() -> bool:
    """Runs a local version of the CI pipeline.

    Useful when remembered.
    :return: Return True on succesful execution, otherwise returns False.
    :rtype: bool
    """

    setup_logging(logging.DEBUG)

    # Format / Lint
    ruff_args = ["ruff", "format"]

    # Type Checking
    mypy_args = ["mypy"]

    # Testing
    test_args = ["pytest"]

    # Security Check
    bandit_args = ["bandit", "-c", "pyproject.toml", "-r", "."]

    list_of_args = [
        (ruff_args, "format checks"),
        (mypy_args, "type checks"),
        (test_args, "tests"),
        (bandit_args, "security checks"),
    ]

    ret_val = True

    try:
        for arg_set, print_statement in list_of_args:
            logger.debug(f"Running {print_statement} now!")
            status = subprocess.call(
                arg_set, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
            )  # nosec B603
            if status == 0:
                logger.debug(f"{print_statement} were successful!")
            else:
                logger.debug(f"{print_statement} failed!")
                ret_val = False
    except Exception as e:
        logger.exception(e)
        ret_val = False
        return ret_val

    if ret_val:
        logger.info("All CI checks have passed!")
    else:
        logger.info("A CI check has failed, please check the logs.")

    return ret_val


def run_pfts(arg_list: list | None = None) -> None:
    """Runs the tool in general command line mode.

    :param arg_list: List of args to use, defaults to None
    :type arg_list: list | None, optional
    """

    # Avoids list gotcha
    # None will result in sys.argv[1:]
    args = parse_input(arg_list)

    log_level = logging.DEBUG if args.dev else logging.WARNING
    setup_logging(log_level)
    logger.info(f"Successfully loaded in the following args: {args}")


def version_bump(arg_list: list | None = None) -> None:
    """Quality of life function to bump the version numbering.

    :param arg_list: CLI Iterface, defaults to None
    :type arg_list: list | None
    """

    # Avoids list gotcha
    # None will result in sys.argv[1:]
    args = parse_input(arg_list)

    log_level = logging.DEBUG if args.dev else logging.WARNING
    setup_logging(log_level)
    logger.info(f"Successfully loaded in the following args: {args}")

    new_version = general.bump_version(args.vbump)
    logger.info(f"New version is: {new_version}")
