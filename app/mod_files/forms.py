from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, DecimalField, TextAreaField, DateField, SelectField, RadioField, SelectMultipleField, HiddenField

from app import datasets
from app.mod_files.models import Keywords, UserFiles

from wtforms.validators import DataRequired, InputRequired, Optional

class Select2MultipleField(SelectMultipleField):

    def pre_validate(self, form):
        # Prevent "not a valid choice" error
        pass

    def process_formdata(self, valuelist):
        if valuelist:
            self.data = ",".join(valuelist)
        else:
            self.data = ""

class FileForm(FlaskForm):
    """docstring for FileForm"""
    def __init__(self, tags, statuses, data, *args, **kwargs):
        super(FileForm, self).__init__()
        self.tags       = tags
        self.statuses   = statuses
        self.metadata   = data

    def get_form(self, *args, **kwargs):
        return BaseForm(self.tags, self.statuses, self.metadata)


class BaseForm(FlaskForm):
    """docstring for FileForm"""

    file                = FileField('File', validators=[FileRequired(), FileAllowed(datasets, 'Datasets only!')])
    title               = StringField('Title', validators=[InputRequired()])
    shortname           = StringField('Short name', validators=[InputRequired()])
    abstract            = TextAreaField('Abstract', validators=[Optional()])
    node_id             = HiddenField('node_id')

    #investigators

    #personnel

    keywords            = Select2MultipleField('Keywords', validators=[InputRequired()])
    additional_keywords = StringField('Additional keywords', validators=[InputRequired()])

    #funding

    #timeframe
    start_date          = DateField('Start date', format='%m/%d/%Y', validators=[InputRequired()])
    end_date            = DateField('End date', format='%m/%d/%Y', validators=[Optional()])
    status              = SelectField('Status', validators=[InputRequired()])

    #geographic location
    geo_description     = TextAreaField('Verbal description', validators=[Optional()])
    northbound          = DecimalField('Northbound', validators=[Optional()])
    southbound          = DecimalField('Southbound', validators=[Optional()])
    eastbound           = DecimalField('Eastbound', validators=[Optional()])
    westbound           = DecimalField('Westbound', validators=[Optional()])

    methods             = TextAreaField('Methods', validators=[Optional()])

    #datatable

    column_name         = StringField('Column name', validators=[Optional()])
    description         = StringField('Description', validators=[Optional()])
    explanation         = StringField('Explanation', validators=[Optional()])
    empty_code          = StringField('Empty value code', validators=[Optional()])

    comments            = TextAreaField('Comments', validators=[Optional()])

    def __init__(self, tags, statuses, data, *args, **kwargs):
        super(BaseForm, self).__init__(data=data, *args, **kwargs)
        self.keywords.choices = tags
        self.status.choices = statuses


class CreateFolderForm(FlaskForm):

    name                = StringField('Folder name', validators=[DataRequired()])
