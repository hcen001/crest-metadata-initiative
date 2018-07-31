from flask import Blueprint, redirect, url_for, abort, render_template, flash, request, session
from flask_login import login_required, current_user
from werkzeug.datastructures import CombinedMultiDict
from werkzeug.utils import secure_filename
from flask_uploads import UploadNotAllowed

from app.mod_files.forms import FileForm
from app.mod_files.models import UserFiles
from app.mod_rest_client.client import NodeClient
from app.mod_rest_client.constants import Nodes, Who

from app import datasets
from app import app
import os
import pprint

pp = pprint.PrettyPrinter(indent=2)

# Define the blueprint
mod_files = Blueprint('files', __name__)

@mod_files.route('/', methods=['GET'])
@login_required
def index():
    js = render_template('files/index.js')
    return render_template('files/index.html', user=current_user, title='Files', js=js)

@mod_files.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():

    if request.method == 'POST':
        form = FileForm()
        if request.files['file'] is not None:
            try:
                filename = datasets.save(request.files['file'])
            except UploadNotAllowed as e:
                flash('File not allowed.', 'danger')
                return redirect(url_for('files.upload'))
            else:
                url = datasets.url(filename)
        else:
            flash('No file was selectec to be uploaded.', 'danger')
            return redirect(url_for('files.upload'))

        filepath = os.path.join(app.root_path, 'static/uploads/datasets/', filename)
        files = {'filedata': open(filepath, 'rb')}

        upload_node = request.form.get('node_id') or Nodes.shared.value

        print('NODE_ID: ', upload_node)

        upload_response = NodeClient().upload(current_user.ticket, files, upload_node)

        if upload_response.status_code == 201:
            flash('File was successfully uploaded to the repository', 'success')
            if os.path.exists(filepath):
                os.remove(filepath)
        else:
            flash('An unexpected error happened while trying to upload the file to the repository', 'danger')
        return redirect(url_for('files.index'))

    js      = render_template('files/upload/wizard.js')
    form    = FileForm()
    tree    = UserFiles().shared_files_tree(whom=Who.all)
    pp.pprint(tree)
    return render_template('files/upload/wizard.html', user=current_user, title='Upload files', form=form, tree=tree, js=js)

@mod_files.route('/shared_by/<node>', methods=['GET'])
@login_required
def shared_by(node):
    tree = UserFiles().shared_files_tree(Who(node))
    js = render_template('files/shared_by/index.js')
    return render_template('files/shared_by/index.html', user=current_user, title='Shared files uploaded by '+node, tree=tree, js=js)

@mod_files.route('/private', methods=['GET'])
@login_required
def private():
    tree = UserFiles().private_files_tree()
    js = render_template('files/shared_by/index.js')
    return render_template('files/shared_by/index.html', user=current_user, title='Private files uploaded', tree=tree, js=js)
