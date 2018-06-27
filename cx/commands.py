# !/usr/bin/env python
# --*--coding:utf-8--*--

# from base64 import b64decode, b64encode
from builtins import input
from getpass import getpass
from os import path, listdir, makedirs, chmod
import errno, os, stat
from shutil import rmtree
from urlparse import urlparse, ParseResult, ResultMixin

from cx import display
from cx.config import (BasicAuthConfig, CommandLineConfig)

from git import Repo

def fail(args):
    display.show_command('fail')

def auth(args):
    params = {
        'config_basedir': args['--config'],
        'set': args['--set'],
        'list': args['--list'],
    }
    display.show_command('auth', params)

    if not params['config_basedir']:
        config_file = CommandLineConfig.config_file()
    else:
        config_file= CommandLineConfig.config_file(basedir=params['config_basedir'])

    if (params['set'] or (
            not params['list'] and
            not path.isfile(config_file))):
        (git_url, git_alias) = git_set_repo()
        (email, auth) = auth_set_basic()
        CommandLineConfig.save_config(email, auth, git_url=git_url, git_alias=git_alias, config_file=config_file)

    all_cfgs = CommandLineConfig.load_all_configs(config_file=config_file)
    for alias, values in all_cfgs.iteritems():
        display.show_config(alias, values)

def git_set_repo():
    git_url = input('Git URL: ');
    git_alias = input('Git Alias: ');
    return (git_url, git_alias)

def auth_set_basic():
    email = input('Email: ')
    username = input('username: ')
    password = getpass()
    auth = BasicAuthConfig(
        username=username,
        password=password)
    return (email, auth)

def clone(args):
     params = {
        'config_basedir': args['--config'],
        'git_alias': args['--git_alias'],
        'fpath': args['<fpath>']
     }
     display.show_command('clone', params)

     if not params['config_basedir']:
         config_file = CommandLineConfig.config_file()
     else:
         config_file= CommandLineConfig.config_file(basedir=params['config_basedir'])

     print config_file

     config = CommandLineConfig(config_file=config_file, git_alias=params['git_alias'])
     username=config.__dict__['username']
     print username
     password=config.__dict__['password']
     print password
     parsed_url = urlparse(config.__dict__['git_url']);
     print parsed_url

     new_netloc = "{}:{}@{}".format(
            username, password, parsed_url.netloc)

     remote = ParseResult(
        scheme=parsed_url.scheme, netloc=new_netloc,
        path=parsed_url.path, params=parsed_url.params,
        query=parsed_url.query, fragment=parsed_url.fragment).geturl()
     fpath = params['fpath']

     if path.exists(fpath) and path.isdir(fpath):
          rmtree(fpath, ignore_errors=False, onerror=handleRemoveReadonly)
     if not path.exists(fpath):
         try:
            makedirs(fpath)
         except OSError as e:
            if e.errno != errno.EEXIST:
                raise

     Repo.clone_from(remote, fpath)


def handleRemoveReadonly(func, path, exc):
    excvalue = exc[1]
    if func in (os.rmdir, os.remove) and excvalue.errno == errno.EACCES:
        os.chmod(path, stat.S_IRWXU| stat.S_IRWXG| stat.S_IRWXO) # 0777
        func(path)
    else:
        raise
#     password_string = base64.b64decode("password")
#     #Repo.clone_from(git_url, repo_dir)
#
# def mask(args):
#     password = args['<password>']
#     display.show_command('mask', 'password=%s' % password)
#     display.show_content(b64encode(password))
