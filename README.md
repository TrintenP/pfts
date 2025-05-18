# Patten's Financial Tool Suite (pfts)
![Static Badge](https://img.shields.io/badge/license-MIT-green) ![Static Badge](https://img.shields.io/badge/python-3.13-blue) <img alt="gitleaks badge" src="https://img.shields.io/badge/protected%20by-gitleaks-blue">

PFTS was created as a personal project that will explore how to code a variety of personal finance tools in Python. 

# Prerequisites
1. Basic command-line knowledge
2. Python 3.13 installed on their machine

# Installation
`pip install pfts`

# General Usage
This project will create a set of entry points that can be used in the console. 

`pfts`: Will parse command line for arguments. 

- Arguments:
    - TBA


# Development Usage
This section is to provide additional information for how to use the developer CLI.

### Commands:
`generate-docs`: Will automatically generate, and open, a local copy of documentation.

`run-testing [--disablecov | ]`: Will run the entire test suite for pfts, generate a coverage report, and open it.

`local-ci`: Run through a local version of the CI pipeline to ensure code is up to standard.

`version-bump --vbump <major|minor|patch>`: Quality of Life script that bumps pfts version.