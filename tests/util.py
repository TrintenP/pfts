"""Utility functions for testing"""

import functools
import os
import pathlib
from typing import Callable


def create_maintainer(filepath: pathlib.Path) -> Callable:
    """Decorator factory that creates a decorator based on the based in file

    :param filepath: Filepath of the file to maintain state for
    :type filepath: pathlib.Path
    :return: Decorator which maintains a defined file state
    :rtype: Callable
    """

    def decorator(func: Callable) -> Callable:
        """Maintains the state of a mock_init file during testing.

        :param _func: Test function.
        :type _func: Callable
        :return: Function that maintains file state.
        :rtype: Callable
        """

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # If file doesn't exist then create it.
            # Rather create new files than crash
            if not filepath.exists():
                # If the parent folder doesn't exist then create
                if not filepath.parent.exists():
                    filepath.parent.mkdir()

                with open(filepath, "w") as fout:
                    ...

            with open(filepath, "r") as fin:
                old_data = fin.readlines()

            try:
                return func(*args, **kwargs)
            finally:
                with open(filepath, "w") as fout:
                    fout.writelines(old_data)

        return wrapper

    return decorator


MOCK_INIT_FILEPATH = pathlib.Path(__file__).parent / "data" / "mock_init.txt"
REAL_INIT_FILEPATH = pathlib.Path(__file__).parents[1] / "pfts" / "__init__.py"
LOG_FILEPATH = pathlib.Path(__file__).parents[1] / "logs" / "app.log"

maintain_mock_init = create_maintainer(MOCK_INIT_FILEPATH)
maintain_real_init = create_maintainer(REAL_INIT_FILEPATH)
maintain_log = create_maintainer(LOG_FILEPATH)
