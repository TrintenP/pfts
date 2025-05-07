# Patten's Financial Tool Suite (pfts)
![Static Badge](https://img.shields.io/badge/license-MIT-green) ![Static Badge](https://img.shields.io/badge/python-3.13-blue) <img alt="gitleaks badge" src="https://img.shields.io/badge/protected%20by-gitleaks-blue">

PFTS was created as a personal project that will explore how to code a variety of personal finance tools in Python. 

- **Documentation**:  https://trintenp.github.io/pfts/
- **Source Code**: https://github.com/TrintenP/pfts
- **Bug Reports**: https://github.com/TrintenP/pfts/issues

## Installation:
- Ensure that Python version installed is 3.13 or better:
    - `python --version`
- Install uv package manager
    - `pip install uv`
- Clone GIT repo
    - `git clone https://github.com/TrintenP/pfts.git`
- Change into Cloned repo
    - `cd pfts` 
- Create virtual environment
    - `uv venv --python 3.13`
- Activate Environment
    - `.venv\Scripts\activate`
- Update virtual environment
    - `uv sync`
- Run commands (See Usage section)
    - `uv run <command>`

## General Usage
This project will create a set of entry points that can be used in the console. 

`pfts`: Will run pfts while parsing command line inputs. 

- Arguements:
    - TBA


## Development Usage
This section is to provide additional information for how to develop ppft further.

Commands:
`generate-docs`: Will automatically generate, and open, a local copy of documentation.

`run-testing`: Will run the entire test suite for pfts, generate a coverage report, and open it.

`local-ci`: Run through a local version of the CI pipeline to ensure code is up to standard.

`version-bump`: Utility tool for increasing the version of pfts.

Adding / Removing packages:
- uv add <packageName>
- uv remove <packageName>

Building project:
- uv build --no-sources
