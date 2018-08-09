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
    node_children           = content_api+"nodes/{}/children"
    node_info               = content_api+"nodes/{}"
    upload                  = content_api+"nodes/{}/children"
    rename_folder           = content_api+"nodes/{}"
    create_folder           = content_api+"nodes/{}/children"
    add_tags                = content_api+"nodes/{}/tags"

class Tag(Enum):
    tags                    = content_api+"tags"
