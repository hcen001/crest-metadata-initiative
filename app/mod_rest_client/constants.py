from enum import Enum

class Nodes(Enum):

    private             = '-my-'
    shared              = '-shared-'

class Who(Enum):

    me                  = 'me'
    others              = 'others'
    all                 = 'all'

class NodeType(Enum):

    folder              = 'cm:folder'

class Action(Enum):

    create_folder       = 'create_folder'
    rename_folder       = 'rename_folder'
    upload              = 'upload'
