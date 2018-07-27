from app import db
from flask_login import current_user
from flask import session
from sqlalchemy.dialects.postgresql import ARRAY, JSON

from app.models import Base, BaseTemplate

from app.mod_rest_client.client import NodeClient
from app.mod_rest_client.constants import Nodes, Who

import pprint
pp = pprint.PrettyPrinter(indent=2)

class CoreMetadata(BaseTemplate):
    """docstring for CoreMetadata"""

    __tablename__ = 'core_metadata'

    investigators           = db.Column('investigators', ARRAY(JSON))
    personnel               = db.Column('personnel', ARRAY(JSON))
    funding                 = db.Column('funding', ARRAY(JSON))
    methods                 = db.Column('methods', db.Text, nullable=True)
    geographic_location     = db.Column('geographic_location', JSON, nullable=True)
    status_id               = db.Column('status_id', db.Integer, db.ForeignKey('status.id'), nullable=False)

    status                  = db.relationship('Status', backref='_datasets', foreign_keys=[status_id], lazy=True)

    def __init__(self, methods=None, geographic_location=None, **kwargs):

        super(CoreMetadata, self).__init__()
        self.investigators              = kwargs.get('investigators')
        self.personnel                  = kwargs.get('personnel')
        self.funding                    = kwargs.get('funding')
        self.methods                    = kwargs.get('methods') or methods
        self.geographic_location        = kwargs.get('geographic_location') or geographic_location
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

class UserFiles(object):
    """docstring for UserFiles"""

    def node_children(self, node=Nodes.shared.value, entries=None):

        if entries is None:
            entries = []

        response = NodeClient().node_children(node, current_user.ticket)

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
        else:
            _ret = [file for file in entries if current_user.username in file['entry']['createdByUser'].values()]

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

        # pp.pprint(tree)

        return tree
        # return {}

    @property
    def private_files(self):
        entries = self.node_children(Nodes.private.value)
        return [file for file in entries if file['entry']['isFolder'] == False]
