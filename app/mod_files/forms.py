from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, TextAreaField, DateField, SelectField, RadioField

from app import datasets

from wtforms.validators import DataRequired, InputRequired, Optional

class FileForm(FlaskForm):
    """docstring for FileForm"""

    file                = FileField('File', validators=[FileRequired(), FileAllowed(datasets, 'Datasets only!')])
    title               = StringField('Title', validators=[InputRequired()])
    shortname           = StringField('Short name', validators=[InputRequired()])
    abstract            = TextAreaField('Abstract', validators=[Optional()])

    #investigators

    #personnel

    keywords            = StringField('Keywords', validators=[InputRequired()])

    #funding

    #timeframe
    start_date          = DateField('Start date', validators=[InputRequired()])
    end_date            = DateField('End date', validators=[InputRequired()])

    #geographic location

    methods             = TextAreaField('Methods', validators=[Optional()])

    #datatable

    column_name         = StringField('Column name', validators=[Optional()])
    description         = StringField('Description', validators=[Optional()])
    explanation         = StringField('Explanation', validators=[Optional()])
    empty_code          = StringField('Empty value code', validators=[Optional()])

    comments            = TextAreaField('Comments', validators=[Optional()])



