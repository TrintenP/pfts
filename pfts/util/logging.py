"""Contains functions in relation to logging."""

import functools
import logging.config
import pathlib
from typing import Callable

logger = logging.getLogger(__name__)

CUSTOM_LOG_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "log_file": {
            "format": "%(asctime)s - %(levelname)s - %(name)s - %(lineno)d - \n\t%(message)s\n",  # noqa: E501
            "datefmt": "%Y-%m-%dT%H:%M:%SZ",
        },
        "log_stream": {
            "format": "%(levelname)s - %(name)s - %(lineno)d - %(message)s"
        },
    },
    "handlers": {
        "debug_file_handler": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": logging.INFO,
            "formatter": "log_file",
            "filename": "./logs/app.log",
            "maxBytes": 100_485_760,
            "backupCount": 3,
            "encoding": "utf8",
            "mode": "a",
        },
        "consoleHandler": {
            "class": "logging.StreamHandler",
            "formatter": "log_stream",
            "level": logging.DEBUG,
        },
    },
    "root": {
        "level": logging.DEBUG,
        "handlers": [
            "debug_file_handler",
            "consoleHandler",
        ],
    },
}


# Context: https://ankitbko.github.io/blog/2021/04/logging-in-python/
def log_context(_func: Callable) -> Callable:
    """Creates a standard logging format.

    Will denote function signature, and if it raises an error.

    :param func: Function to be logged.
    :type func: Callable
    :return: Function with standardized logging.
    :rtype: Callable
    """

    def decorator_log(func):
        # Allows the wrapped function to maintain its properties.
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            args_repr = [repr(a) for a in args]
            kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
            signature = ", ".join(args_repr + kwargs_repr)
            logger.debug(
                f"Function {func.__name__} called with args {signature}"
            )
            try:
                returned_val = func(*args, **kwargs)
                return returned_val
            except Exception as e:
                logger.exception(
                    f"Exception raised in {func.__name__}. Exception: {str(e)}"
                )
                returned_val = None
                raise e
            finally:
                logger.debug(
                    f"Function {func.__name__} returned: {returned_val}"
                )

        return wrapper

    return decorator_log(_func)


def setup_logging(log_level=0) -> None:
    """Setup logging configuration, reading in from log cfg file if possible.

    :param log_level: Specify the level logs that are required, defaults to 0
    :type log_level: int, optional
    """
    generate_log_location()

    logging.config.dictConfig(CUSTOM_LOG_CONFIG)
    logger.setLevel(log_level)
    logger.info("Successfully loaded in logging configs.")


def generate_log_location(log_path: pathlib.Path | None = None) -> None:
    """If logs folder doesn't exist, then create it."""

    if log_path is None:
        # Create log dir in the root of the module
        log_path = pathlib.Path(__file__).parents[2] / "logs"

    if not log_path.exists():
        log_path.mkdir(exist_ok=True)


def process_logging(logger: logging.Logger, retcode: int, name: str) -> bool:
    """Takes a subprocess returncode and human-readable name.
    Logs status of the process and returns good or bad.

    :param logger: Logger to use when writing logs.
    :type logger: logging.Logger
    :param retcode: The return value from a given process.
    :type retcode: int
    :param name: The human readable name of the process.
    :type name: str
    :return: Returns True if process returns 0.
    :rtype: bool
    """

    if retcode != 0:
        logger.warning(
            f"Something went wrong with {name} returned value of {retcode}."
        )
        rtn_status = False
    else:
        logger.info(f"Successfully ran {name}")
        rtn_status = True

    return rtn_status
