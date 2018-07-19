from simple_rest_client.api import API
from enum import Enum

from app.mod_rest_client.actions import AuthResource, PeopleResource, NodesResource
from flask_login import current_user
from flask import flash, redirect, url_for

API_ROOT_URL = 'http://ralph.cs.fiu.edu:8080/'

class Services(Enum):
    """docstring for Services"""
    auth        = 'auth'
    people      = 'people'
    node        = 'node'


class Client(object):
    """docstring for Client"""

    def __init__(self):
        self.api = API(
            api_root_url = API_ROOT_URL,
            params = {},
            headers = {},
            timeout = 2,
            append_slash = False,
            json_encode_body=True
        )

    def request(self):
        return self

    def test(self):
        self.api.add_resource(resource_name='auth', resource_class=AuthResource)
        response = self.api.auth.login(body={'username': 'admin', 'password': 'admin'})
        print('***RESPONSE***')
        if response.status_code == 200:
            print(response.body['data'])
        return response.body

class AuthClient(Client):
    """docstring for AuthClient"""
    def __init__(self):
        super(AuthClient, self).__init__()
        if Services.auth.value not in self.api.get_resource_list():
            self.api.add_resource(resource_name=Services.auth.value, resource_class=AuthResource)

    def login(self, username, password):
        try:
            response = self.api.auth.login(body={'username': username, 'password': password})
        except Exception as e:
            print('**RESPONSE**', e.response)
            return e.response
        else:
            return response

    def logout(self, ticket):
        try:
            response = self.api.auth.logout(ticket, params={'alf_ticket': ticket})
        except Exception as e:
            return e.response
        else:
            return response

class PeopleClient(Client):
    """docstring for PeopleClient"""
    def __init__(self):
        super(PeopleClient, self).__init__()
        if Services.people.value not in self.api.get_resource_list():
            self.api.add_resource(resource_name=Services.people.value, resource_class=PeopleResource)

    def userinfo(self, user, ticket):
        try:
            response = self.api.people.info(user, body=None, params={'alf_ticket': ticket}, headers={})
        except Exception as e:
            return e.response
        else:
            return response

class NodeClient(Client):
    """docstring for NodeClient"""
    def __init__(self):
        super(NodeClient, self).__init__()
        if Services.node.value not in self.api.get_resource_list():
            self.api.add_resource(resource_name=Services.node.value, resource_class=NodesResource)

    def private_filelist(self, ticket):
        try:
            response = self.api.node.private_list(body=None, params={'alf_ticket': ticket}, headers={})
        except Exception as e:
            return e.response
        else:
            return response

    def shared_filelist(self, ticket):
        try:
            response = self.api.node.shared_list(body=None, params={'alf_ticket': ticket}, headers={})
        except Exception as e:
            return e.response
        else:
            return response
