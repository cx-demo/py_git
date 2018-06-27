# !/usr/bin/env python
# --*--coding:utf-8--*--

"""
A command-line interface to clone GIT repository

Usage:
cxclone.py auth [-c <config_basedir>|--config=<config_basedir>] [(--set|--list)]
cxclone.py clone [-c <config_basedir>|--config=<config_basedir>] [--git_alias=<git_alias>] <fpath>
cxclone.py -h|--help
cxclone.py -v|--version

Arguments:
fpath  Folder path to clone into

Options:
-c <config_basedir> --config=<config_basedir>  Config file base directory i.e., <config_basedir>\.cx\cxclone.json
--set  Set credential
--list  List credential
--git_url=<git_url>  Git repository
--git_alias=<git_alias>  Git alias
-h --help  show this screen.
-v --version  Print the version.

"""
# -i FILE --input FILE  Specify input file

from docopt import docopt

from cx import metadata
from cx import commands
from cx.utils import get_first
from cx.display import show_server_error

def is_command(s):
    if s.startswith('-'):
        return False
    if s.startswith('<'):
        return False
    return True

def dispatch_command(arguments, command='fail'):
    f = getattr(commands, "{}".format(command), commands.fail)
    return f(arguments)

def main():
    version_string = '{0} {1}'.format(metadata.project, metadata.version)
    arguments = docopt(__doc__, version=version_string)
    print arguments
    command = get_first([
        k for (k, v) in arguments.iteritems()
        if (v and is_command(k))])
    # try:
    dispatch_command(arguments, command)
    # except ServerError as e:
    #     show_server_error(e)


if __name__ == '__main__':
    main()
