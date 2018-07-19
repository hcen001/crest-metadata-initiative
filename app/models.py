from app import db
from sqlalchemy.exc import IntegrityError

import json

# Define a base model for other database tables to inherit
class Base(db.Model):

    __abstract__ = True

    id           = db.Column(db.Integer, primary_key=True)
    date_created = db.Column('date_created', db.DateTime, default=db.func.current_timestamp())
    date_updated = db.Column('date_updated', db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    active       = db.Column('active', db.Boolean, default=True, server_default='t')

    def add_or_update(self, deactivate=None, reactivate=None):

        if deactivate is not None and deactivate == True:
            self.active = False

        if reactivate is not None and reactivate == True:
            self.active = True

        try:
            db.session.add(self)
            db.session.flush()
        except IntegrityError as e:
            raise

    def update(self, data):
        self.query.update(data)

    def save(self):
        db.session.commit()
        db.session.expire_all()

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

class PersonBase(Base):

    __abstract__ = True

    first_name   = db.Column('first_name', db.String(128), nullable=False, default='First name', server_default='First name')
    last_name    = db.Column('last_name', db.String(128), nullable=False, default='Last name', server_default='Last name')
    email        = db.Column('email', db.String(128), nullable=False, default='someone@xample.org', server_default='someone@xample.org', unique=True)

    @property
    def full_name(self):
        return self.first_name+' '+self.last_name
