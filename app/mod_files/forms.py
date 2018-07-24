from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from flask_uploads import UploadSet
from werkzeug.utils import secure_filename
from app import datasets

from wtforms import StringField, TextAreaField, DateField, SelectField, RadioField
from wtforms.validators import DataRequired, InputRequired, Optional

class FileForm(FlaskForm):
    """docstring for FileForm"""

    file = FileField('File', validators=[FileRequired(), FileAllowed(datasets, 'Datasets only!')])
