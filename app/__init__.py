from flask import Flask

app = Flask(__name__, instance_relative_config=True, static_folder='static')

# Load the default configuration
app.config.from_object('config.default')

# Load the configuration from the instance folder
# app.config.from_pyfile('config.py')

# Load the file specified by the APP_CONFIG_FILE environment variable
# Variables defined here will override those in the default configuration
app.config.from_envvar('APP_CONFIG_FILE')

# Load database
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy(app, session_options={"expire_on_commit": True})
# db.sessionmaker(autoFlush=True)
# db.session.connection(execution_options={'isolation_level': "READ COMMITTED"})
migrate = Migrate(app, db)

# Load Login manager
from flask_login import LoginManager
login = LoginManager()
login.init_app(app)
login.login_view = 'auth.login'
login.login_message_category = "danger"

# Register blueprint(s)
from app.mod_auth.controllers import mod_auth as auth_module
app.register_blueprint(auth_module, url_prefix='/auth')

from app.mod_dashboard.controllers import entry_point
app.register_blueprint(entry_point)

@app.shell_context_processor
def make_shell_context():
    from app.mod_auth.models import User

    return {'db': db, 'User': User}