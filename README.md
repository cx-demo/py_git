PYGIT
===============

*PYGIT: A utility to clone source code from repository

Version:  1.0  
Author:   Pedric Kng

# Running

## Pre-requisites
- gitclient (installed separately)

## Usage

```bash
py_git.py [args ...]

Arguments:

Options:  
--help Show help
--verbose Print more text
--version Show version.

```

# Build

## Installing Gitpython
Installing GitPython is easily done using pip. Assuming it is installed, just run the following from the command-line:
```bash
# pip install gitpython
```
This command will download the latest version of GitPython from the Python Package Index and install it to your system.

##  Packaged as Windows Executable

Requires pyinstaller  
```bash
pip install pyinstaller
```

Packaging
```bash
pyinstaller myscript.py
```

# License
This utility is free-for-use
