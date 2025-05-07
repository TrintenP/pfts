"""Tests written for the general package of pfts."""

import pytest

import pfts
from pfts.util import general, parsing
from tests.util import MOCK_INIT_FILEPATH, maintain_log, maintain_mock_init


@maintain_log
def test_return_true():
    """Ensure pfts is in context."""
    assert general.return_true()


@maintain_log
@pytest.mark.parametrize(
    "str_input, expected",
    [
        ("__version__ = '0.0.0'\n", [0, 0, 0]),
        ("__version__ = '1.2.3'\n", [1, 2, 3]),
        ("__version__ = '0.1.0'\n", [0, 1, 0]),
    ],
)
def test_split_version_line(str_input: str, expected: list):
    expected_version = {
        "major": expected[0],
        "minor": expected[1],
        "patch": expected[2],
    }
    result = general.split_version_line(str_input)
    assert result == expected_version


@maintain_log
@maintain_mock_init
def test_insert_into_full_file():
    index = parsing.parse_init_file(MOCK_INIT_FILEPATH)

    with open(MOCK_INIT_FILEPATH, "r") as fin:
        rest = fin.readlines()

    new_line = "__version__ = '3.2.1'\n"

    general.insert_into_file(MOCK_INIT_FILEPATH, new_line, rest, index)

    with open(MOCK_INIT_FILEPATH, "r") as fin:
        new_lines = fin.readlines()

        assert new_lines[index] == new_line


@maintain_log
@maintain_mock_init
def test_insert_into_empty_file():
    """Verifies that having an empty file doesn't break the function."""
    MOCK_INIT_FILEPATH.unlink()

    general.insert_into_file(
        MOCK_INIT_FILEPATH, "__version__ = '0.0.0'", [], 0
    )

    index = parsing.parse_init_file(MOCK_INIT_FILEPATH)
    assert index == 0


@maintain_log
def test_bump_version_invalid_version():
    version = pfts.__version__
    new_version = general.bump_version("mjr", True)
    assert version == new_version


@maintain_log
@maintain_mock_init
@pytest.mark.parametrize("part", [("major"), ("minor"), ("patch")])
def test_bump_version_valid_version(part: str):
    version_index = parsing.parse_init_file(MOCK_INIT_FILEPATH)

    with open(MOCK_INIT_FILEPATH, "r") as fin:
        version = fin.readlines()[version_index]

    expected = general.split_version_line(version)
    expected[part] += 1

    new_version = general.bump_version(part, True)
    new_line = f"__version__ = '{new_version}'"
    result = general.split_version_line(new_line)

    assert expected == result


@maintain_log
@maintain_mock_init
def test_consecutive_bumps():
    """Created after a bug was discovered that multiple
    bumps created many __version__ lines."""
    general.bump_version("major", True)
    general.bump_version("minor", True)
    general.bump_version("patch", True)

    version_line_count = 0

    with open(MOCK_INIT_FILEPATH, "r") as fin:
        for line in fin.readlines():
            if "__version__" in line:
                version_line_count += 1

    assert version_line_count == 1


@maintain_log
@maintain_mock_init
@pytest.mark.parametrize(
    "part, expected",
    [("major", "1.0.0"), ("minor", "0.1.0"), ("patch", "0.0.1")],
)
def test_version_bump_missing_init_file(part, expected):
    MOCK_INIT_FILEPATH.unlink()

    version_info = general.bump_version(part, True)
    assert version_info == expected
