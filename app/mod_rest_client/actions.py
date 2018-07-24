from simple_rest_client.resource import Resource

from app.mod_rest_client.endpoints import Auth, People, Node

class AuthResource(Resource):
    """docstring for AuthResource"""
    actions = {
        'login': {'method': 'POST', 'url': Auth.login.value},
        'logout': {'method': 'DELETE', 'url': Auth.logout.value},
        'authenticate': {'method': 'GET', 'url': Auth.authenticate.value}
    }

class PeopleResource(Resource):
    """docstring for PeopleResource"""
    actions ={
        'info' : {'method': 'GET', 'url': People.userinfo.value}
    }

class NodesResource(Resource):
    """docstring for NodesResource"""
    actions = {
        'private_list': {'method': 'GET', 'url': Node.private_nodelist.value},
        'shared_list': {'method': 'GET', 'url': Node.shared_nodelist.value},
        'shared_folder_info': {'method': 'GET', 'url': Node.shared_folder_info.value},
        'upload': {'method': 'POST', 'url': Node.upload.value}
    }

