# -*- coding: utf-8 -*-

"""
Classes for abstracting over different forms of GIT authentication.

"""

class Authenticator(object):

    def get_username(self):
        return ""

    def __init__(self, server_base_uri=None):
        self.server_base_uri = server_base_uri or 'http://mygit.com'

class Anonymous(Authenticator):
    pass

class BasicAuthenticator(Authenticator):

    def get_username(self):
        return self.username

    def __init__(
            self,
            username,
            password,
            client_email,
            server_base_uri=None):
        self.username = username
        self.password = password
        self.client_email = client_email
        super(BasicAuthenticator, self).__init__(
                server_base_uri=server_base_uri,
        )
