"""Tests written for the logging of pfts."""

import logging
import pathlib

import pytest

from pfts.util import logging as pfts_log
from tests.util import maintain_log

LOGGER = logging.getLogger(__name__)


@maintain_log
@pytest.fixture
def process_log_fixture(request, caplog):
    """Allows for indirect parametrization."""
    returncode, name = request.param
    pfts_log.process_logging(LOGGER, returncode, name)

    return (returncode, name, caplog.records)


@maintain_log
def test_process_logging_good_return(caplog):
    pfts_log.process_logging(LOGGER, 0, "test_code")

    for record in caplog.records:
        assert record.levelname == "INFO"
        assert "Successfully ran test_code" in record.message


@pytest.mark.parametrize(
    "process_log_fixture",
    [(1, "test_code"), (15, "test_code"), (-1, "test_code")],
    ids=["Bad_Return", "Different_Bad_Return", "Negative_Return"],
    indirect=True,
)
@maintain_log
def test_process_logging_bad_returns(process_log_fixture):
    returncode, name, logs = process_log_fixture

    for record in logs:
        assert record.levelname == "WARNING"
        assert (
            f"Something went wrong with {name} returned value of {returncode}"
        )


@maintain_log
def test_generate_log_missing_log_directory():
    test_loc = pathlib.Path(__file__).parent / "data" / "log"

    # Used to clean up if a previous test failed.
    if test_loc.exists():
        test_loc.rmdir()

    pfts_log.generate_log_location(test_loc)
    assert test_loc.exists()
    test_loc.rmdir()


@maintain_log
def test_generate_log_existing_directory():
    test_loc = pathlib.Path(__file__).parent / "data" / "log"
    test_loc.mkdir(exist_ok=True)

    pfts_log.generate_log_location(test_loc)
    test_loc.rmdir()

    # Just used to make sure that generation doesn't crash
    assert True


@maintain_log
def test_generate_log_default_location():
    pfts_log.generate_log_location()

    log_path = pathlib.Path(__file__).parents[1] / "logs"

    assert log_path.exists()


@maintain_log
def test_setup_logging_file_logging(caplog, capsys):
    pfts_log.setup_logging()

    # Will log once in the info level file
    for record in caplog.records:
        assert record.levelname == "INFO"
        assert "Successfully loaded in logging configs." in record.message

    # Will log once using the stream handler
    assert "Successfully loaded in logging configs." in capsys.readouterr().err


@maintain_log
def test_log_context_normal_function(capsys):
    pfts_log.setup_logging(10)

    @pfts_log.log_context
    def normal_func(a, b):
        return a + b

    normal_func(1, 2)

    # Debug level errors will only show up in stderr
    captured_messages = capsys.readouterr().err.lower()

    assert "function normal_func called with args 1, 2" in captured_messages
    assert "function normal_func returned: 3" in captured_messages


@maintain_log
def test_log_context_exception(capsys):
    pfts_log.setup_logging(10)

    @pfts_log.log_context
    def raise_exception():
        raise Exception

    with pytest.raises(Exception):
        raise_exception()

    # Debug level errors will only show up in stderr
    captured_messages = capsys.readouterr().err.lower()

    assert "function raise_exception called with args " in captured_messages
    assert (
        "exception raised in raise_exception. exception: " in captured_messages
    )
