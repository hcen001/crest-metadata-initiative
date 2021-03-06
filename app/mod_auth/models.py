from app.models import Base, PersonBase
from app import db, login

# Define a User model
class User(PersonBase):

    __tablename__ = 'user_account'

    # Identification Data: email & password
    username         = db.Column(db.String(64), nullable=False, unique=True)
    authenticated    = db.Column(db.Boolean, nullable=False, server_default='f', default=False)
    ticket           = db.Column(db.String(64), nullable=True)

    # New instance instantiation procedure
    def __init__(self, ticket, **kwargs):
        self.email              = kwargs.get('email')
        self.first_name         = kwargs.get('firstName')
        self.last_name          = kwargs.get('lastName')
        self.username           = kwargs.get('userName')
        self.authenticated      = False
        self.ticket             = None

    def authenticate(self, ticket):
        self.authenticated = True
        self.ticket = ticket
        db.session.add(self)
        db.session.commit()

    def logout(self):
        self.authenticated = False
        self.ticket = None
        db.session.add(self)
        db.session.commit()

    def is_admin(self):
        pass

    @property
    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated

    @property
    def alf_ticket(self):
        """Return the alf_ticket token used to communicate with Alfresco backend."""
        return self.ticket

    @property
    def is_active(self):
        """Always True, as all users are active."""
        return self.active

    @property
    def is_anonymous(self):
        """Always False, as anonymous users aren't supported."""
        return False

    def get_id(self):
    #     """Return the email address to satisfy Flask-Login's requirements."""
    #     """Requires use of Python 3"""
        return str(self.id)

    @classmethod
    def list(cls):

        _users = cls.query.all()
        users = []

        for _user in _users:
            user = {}
            user['name'] = _user.full_name
            user['email'] = _user.email
            user['active'] = _user.active
            user['authenticated'] = _user.authenticated
            user['added_date'] = _user.date_created
            users.append(user)

        return users

    def __repr__(self):
        return '<User: email={}, name={}>'.format(self.email, self.full_name)

@login.user_loader
def load_user(user_id):
    return User.query.get(user_id)
