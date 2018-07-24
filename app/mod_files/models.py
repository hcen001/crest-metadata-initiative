from app import db
from sqlalchemy.dialects.postgresql import ARRAY, JSON

from app.models import Base, BaseTemplate

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
