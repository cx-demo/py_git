# -*- coding: utf-8 -*-
import json
from os import getenv, path, makedirs

from cx import metadata

class BaseConfig(object):
    @staticmethod
    def git_url():
        return getenv('GIT_URL', 'https://git-scm.com')


class BasicAuthConfig(BaseConfig):
    def __init__(
            self,
            username=None,
            password=None):
        self.username = username
        self.password = password

    def get_authenticator(self, email, git_url=None):
        if git_url is None:
            git_url = self.git_url()
        return BasicAuthenticator(
            self.username,
            self.password,
            email,
            git_url=git_url)

class CommandLineConfig(object):
    @staticmethod
    def git_url():
        return getenv('GIT_URL', 'https://git-scm.com')

    @staticmethod
    def git_alias():
        return 'git'

    @staticmethod
    def config_file(
            basedir='~',
            appdir='.'+metadata.package,
            filename='cxclone.json'):
        config_path = path.expanduser(path.join(basedir, appdir))
        return path.join(config_path, filename)

    @staticmethod
    def load_all_configs(config_file=None):
        print ("load_all_configs: "+config_file)
        if not config_file:
            config_file = CommandLineConfig.config_file()
        all_cfgs = dict()
        if path.isfile(config_file):
            with open(config_file, 'r') as f:
                all_cfgs = json.load(f)
        return all_cfgs

    @staticmethod
    def load_config(
            config_file=None,
            git_alias=None):
        if not git_alias:
            git_alias = CommandLineConfig.git_alias()
        if not config_file:
            config_file = CommandLineConfig.config_file()
        d = {
            'alias': 'git',
            'git_url': 'https://git-scm.com',
            'username': 'testuser',
            'password': 'secret',
            'client_email': 'testuser@mailme.com'
        }
        all_cfgs = CommandLineConfig.load_all_configs(config_file=config_file)
        if all_cfgs.get(git_alias):
            cfg = all_cfgs[git_alias]
            d['alias'] = git_alias
            d['git_url'] = cfg['git_url']
            d['client_email'] = cfg['email']
            d['username'] = cfg['auth']['HTTPBasicAuth']['username']
            d['password'] = cfg['auth']['HTTPBasicAuth']['password']
        return d

    @staticmethod
    def save_config(
            email,
            auth,
            config_file=None,
            git_url=None,
            git_alias=None):
        if not git_url:
            git_url = CommandLineConfig.git_url()
        if not git_alias:
            git_alias = CommandLineConfig.git_alias()
        if not config_file:
            config_file = CommandLineConfig.config_file()
        print config_file
        d = {
            'git_url':git_url,
            'email': email,
            'auth': {
                'HTTPBasicAuth': {
                    'username': auth.username,
                    'password': auth.password
                }
            }
        }
        try:
            makedirs(path.dirname(config_file))
        except OSError:
            if not path.isdir(path.dirname(config_file)):
                raise
        with open(config_file, 'a+') as f:
            all_cfgs = dict()
            if path.getsize(config_file) > 0:
                all_cfgs = json.load(f)
            all_cfgs[git_alias] = d
            json.dump(all_cfgs, f)

    def __init__(
            self,
            config_file=None,
            git_alias=None):
        if not git_alias:
            git_alias = CommandLineConfig.git_alias()
        if not config_file:
            config_file = CommandLineConfig.config_file()

        d = CommandLineConfig.load_config(
            config_file=config_file,
            git_alias=git_alias)
        self.__dict__ = d
