from enum import Enum

webscript_api   = 'alfresco/s/api/'
content_api     = 'alfresco/api/-default-/public/alfresco/versions/1/'

class Auth(Enum):
    """docstring for People"""
    login           = webscript_api+"login"
    logout          = webscript_api+"login/ticket/{}"
    authenticate    = webscript_api+"login/ticket/{}"

class People(Enum):
    """docstring for People"""
    userinfo        = webscript_api+"people/{}"

class Node(Enum):
    private_nodelist        = content_api+"nodes/-my-/children"
    shared_nodelist         = content_api+"nodes/-shared-/children"
