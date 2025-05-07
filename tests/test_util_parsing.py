"""Tests written for the parsing package of pfts."""

import pathlib
import sys
from argparse import Namespace

import pytest

from pfts.util import parsing
from tests.util import maintain_log, maintain_real_init


@maintain_log
@pytest.mark.parametrize(
    "input,expected",
    [
        ([], Namespace(dev=False, disablecov=False, vbump=None)),
        (["--dev"], Namespace(dev=True, disablecov=False, vbump=None)),
        (["--disablecov"], Namespace(dev=False, disablecov=True, vbump=None)),
        (
            ["--disablecov", "--dev"],
            Namespace(dev=True, disablecov=True, vbump=None),
        ),
        (["-v"], Namespace(dev=False, disablecov=False, vbump="patch")),
        (["--vbump"], Namespace(dev=False, disablecov=False, vbump="patch")),
        (
            ["-v", "major"],
            Namespace(dev=False, disablecov=False, vbump="major"),
        ),
        (
            ["-v", "minor"],
            Namespace(dev=False, disablecov=False, vbump="minor"),
        ),
        (
            ["-v", "patch"],
            Namespace(dev=False, disablecov=False, vbump="patch"),
        ),
        (
            ["--dev", "-v", "major", "--disablecov"],
            Namespace(dev=True, disablecov=True, vbump="major"),
        ),
        (
            ["--dev", "--vbump", "--disablecov"],
            Namespace(dev=True, disablecov=True, vbump="patch"),
        ),
    ],
    ids=[
        "empty",
        "dev_only",
        "cov_only",
        "disable_dev",
        "short_v",
        "full_v",
        "v_major",
        "v_minor",
        "v_patch",
        "All",
        "All_vbump_zero_arg",
    ],
)
def test_parse_input_all_valid_from_list(input: list, expected: Namespace):
    args = parsing.parse_input(input)

    assert args == expected


@maintain_log
@maintain_real_init
def test_parse_input_from_cli(monkeypatch):
    with monkeypatch.context() as m:
        m.setattr(sys, "argv", ["pfts", "--dev", "--vbump"])
        args = parsing.parse_input()
        assert args == Namespace(dev=True, disablecov=False, vbump="patch")


@maintain_log
@pytest.mark.parametrize(
    "input, expected",
    [
        (pathlib.Path("fakepath.txt"), -1),
        (pathlib.Path("tests/data/blank_init.txt"), -1),
        (pathlib.Path("tests/data/mock_init.txt"), 3),
    ],
    ids=["bad_file_name", "empty_file", "good_file"],
)
def test_parse_init_file(input: pathlib.Path, expected):
    assert parsing.parse_init_file(input) == expected
