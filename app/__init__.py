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

#Flask-Uploads
from flask_uploads import UploadSet, configure_uploads
# app.config['UPLOADED_DATASETS_DEST'] = 'uploads'
datasets = UploadSet('datasets', ('csv','xls','xlsx','zip'))
configure_uploads(app, datasets)

# Register blueprint(s)
from app.mod_auth.controllers import mod_auth as auth_module
app.register_blueprint(auth_module, url_prefix='/auth')

from app.mod_dashboard.controllers import entry_point
app.register_blueprint(entry_point)

from app.mod_files.controllers import mod_files
app.register_blueprint(mod_files, url_prefix='/files')

@app.shell_context_processor
def make_shell_context():
    from app.mod_auth.models import User
    from app.mod_files.models import CoreMetadata, Status, UserFiles, Keywords

    return {'db': db, 'User': User, 'datasets': datasets, 'CoreMetadata': CoreMetadata, \
            'Status': Status, 'UserFiles': UserFiles, 'Keywords': Keywords}
