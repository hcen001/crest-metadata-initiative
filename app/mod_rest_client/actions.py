from simple_rest_client.resource import Resource

from app.mod_rest_client.endpoints import Auth, People, Node, Tag

class AuthResource(Resource):
    """docstring for AuthResource"""
    actions = {
        'login':            {'method': 'POST', 'url': Auth.login.value},
        'logout':           {'method': 'DELETE', 'url': Auth.logout.value},
        'authenticate':     {'method': 'GET', 'url': Auth.authenticate.value}
    }

class PeopleResource(Resource):
    """docstring for PeopleResource"""
    actions ={
        'info' :            {'method': 'GET', 'url': People.userinfo.value}
    }

class NodesResource(Resource):
    """docstring for NodesResource"""
    actions = {
        'node_children':    {'method': 'GET',   'url': Node.node_children.value},
        'node_info':        {'method': 'GET',   'url': Node.node_info.value},
        'upload':           {'method': 'POST',  'url': Node.upload.value},
        'rename_folder':    {'method': 'PUT',   'url': Node.rename_folder.value},
        'create_folder':    {'method': 'POST',  'url': Node.create_folder.value},
        'add_tags':         {'method': 'POST',  'url': Node.add_tags.value}
    }

class TagsResource(Resource):
    actions = {
        'tags':             {'method': 'GET', 'url': Tag.tags.value}
    }