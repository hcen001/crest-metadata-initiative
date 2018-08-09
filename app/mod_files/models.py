from app import db
from flask_login import current_user
from flask import session
from sqlalchemy.dialects.postgresql import JSON, ARRAY

from app.models import Base, BaseTemplate, CastingArray

from app.mod_rest_client.client import NodeClient, TagClient
from app.mod_rest_client.constants import Nodes, Who

import pprint
pp = pprint.PrettyPrinter(indent=2)

class CoreMetadata(BaseTemplate):
    """docstring for CoreMetadata"""

    __tablename__ = 'core_metadata'

    investigators           = db.Column('investigators', CastingArray(JSON))
    personnel               = db.Column('personnel', CastingArray(JSON))
    funding                 = db.Column('funding', CastingArray(JSON))
    methods                 = db.Column('methods', db.Text, nullable=True)
    geographic_location     = db.Column('geographic_location', JSON, nullable=True)
    node_id                 = db.Column('node_id', db.String(64), nullable=False)
    status_id               = db.Column('status_id', db.Integer, db.ForeignKey('status.id'), nullable=False)

    status                  = db.relationship('Status', backref='_datasets', foreign_keys=[status_id], lazy=True)

    def __init__(self, *args, **kwargs):

        super(CoreMetadata, self).__init__()
        self.title                      = kwargs.get('dataset_title')
        self.shortname                  = kwargs.get('dataset_shortname')
        self.abstract                   = kwargs.get('abstract')
        self.comments                   = kwargs.get('comments')
        self.keywords                   = kwargs.get('keywords')
        self.start_date                 = kwargs.get('start_date')
        self.end_date                   = kwargs.get('end_date')
        self.datatable                  = kwargs.get('datatable')
        self.investigators              = kwargs.get('investigators')
        self.personnel                  = kwargs.get('personnel')
        self.funding                    = kwargs.get('funding')
        self.node_id                    = kwargs.get('node_id')
        self.methods                    = kwargs.get('methods')
        self.geographic_location        = kwargs.get('geographic_location')
        self.status_id                  = kwargs.get('status_id')

class Status(Base):
    """docstring for Status"""

    __tablename__ = 'status'

    name            = db.Column(db.String(64), nullable=False)
    description     = db.Column(db.String(128), nullable=False)

    def __init__(self, **kwargs):
        super(Status, self).__init__()
        self.name           = kwargs.get('name')
        self.description    = kwargs.get('description')

    @classmethod
    def select_list(cls):
        statuses = cls.query.filter(cls.active == True)
        data = [(status.id, status.name) for status in statuses]
        data.insert(0,('',''))
        return data

class UserFiles(object):
    """docstring for UserFiles"""

    def node_children(self, node=Nodes.shared.value, entries=None):

        _entries = []

        if entries is None:
            entries = []

        response = NodeClient().node_children(node, current_user.ticket)

        if response.status_code == 200:
            _entries = response.body['list']['entries']

        for entry in _entries:
            if entry['entry']['isFolder']:
                entries.append(entry)
                self.node_children(entry['entry']['id'], entries)
            else:
                entries.append(entry)

        return entries

    def add_to_tree(self, root, entry):

        root_id = root.get('id')

        if entry['entry']['parentId'] == root_id:
            if entry['entry']['isFolder']:
                root.get('children').append({"id": entry['entry']['id'], "name": entry['entry']['name'], "children": []})
            if entry['entry']['isFile']:
                root.get('children').append({"id": entry['entry']['id'], "name": entry['entry']['name']})

        if entry['entry']['parentId'] != root_id:
            for child in root.get('children'):
                if child.get('children') is not None:
                    self.add_to_tree(child, entry)

    def node_tree(self, entries, root):

        while entries:
            entry = entries.pop(0)
            self.add_to_tree(root, entry)

    def shared_files_by(self, whom=Who.me, entries=None, filter_folders=False):

        _ret = []

        if entries is None:
            entries = self.node_children()

        if whom == Who.others:
            _ret = [file for file in entries if current_user.username not in file['entry']['createdByUser'].values()]
        if whom == Who.me:
            _ret = [file for file in entries if current_user.username in file['entry']['createdByUser'].values()]
        if whom == Who.all:
            _ret = [file for file in entries]

        if filter_folders:
            return [file for file in _ret if file['entry']['isFile']]
        return _ret

    def shared_files_tree(self, whom=Who.me):

        root_id = session['shared_folder_node_id']
        all_entries = self.node_children()

        tree = {}
        tree['root'] = {"id": root_id, "name": "Shared folder root", "children": []}

        entries = self.shared_files_by(whom, all_entries)

        self.node_tree(entries, tree['root'])

        return tree

    @property
    def private_files(self):
        entries = self.node_children(Nodes.private.value)
        return [file for file in entries if file['entry']['isFolder'] == False]

    def private_files_tree(self):
        all_entries = self.node_children(Nodes.private.value)
        root_id = session['private_folder_node_id']
        tree = {}
        tree['root'] = {"id": root_id, "name": "Private folder root", "children": []}

        self.node_tree(all_entries, tree['root'])

        return tree

class Keywords(object):
    """docstring for Tags"""

    @classmethod
    def taglist(cls):
        response = TagClient().tags(current_user.ticket)
        if response.status_code == 200:
            data = response.body['list']['entries']
            return [(entry['entry']['tag'], entry['entry']['tag']) for entry in data]
        return []
