from flask import Blueprint, redirect, url_for, abort, render_template, flash, request, session, jsonify
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from flask_uploads import UploadNotAllowed

from .forms import CreateFolderForm, FileForm
from .models import UserFiles, Keywords, Status, CoreMetadata
from app.mod_rest_client.client import NodeClient
from app.mod_rest_client.constants import Nodes, Who, NodeType, Action
from app.mod_utils.utils import parse_multi_form, get_list

from app import datasets, app, db

import os
import pprint
import json
from datetime import datetime

pp = pprint.PrettyPrinter(indent=2)

# Define the blueprint
mod_files = Blueprint('files', __name__)

@mod_files.route('/', methods=['GET'])
@login_required
def index():
    shared_files_tree = UserFiles().shared_files_tree(Who.all)
    js = render_template('files/index.js')
    form = CreateFolderForm(formdata=None)
    return render_template('files/index.html', user=current_user, title='Shared files', shared_files_tree=shared_files_tree, form=form, js=js)

@mod_files.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():

    if request.method == 'POST':

        request_data = parse_multi_form(request.form)
        node_id = ''

        ###########FILE UPLOAD###########

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

        upload_response = NodeClient().upload(current_user.ticket, files, upload_node)

        if upload_response.status_code == 201:
            node_id = upload_response.body['entry']['id']
            flash('File was successfully uploaded to the repository', 'success')
            if os.path.exists(filepath):
                os.remove(filepath)
        else:
            flash('An unexpected error happened while trying to upload the file to the repository', 'danger')

        ###########FILE UPLOAD###########

        ############TAG ADDING###########
        all_keywords = request.form.getlist('keywords') + request_data.get('additional_keywords').split(',')
        added_tags = get_list([{"tag": keyword} for keyword in all_keywords])
        add_tag_response = NodeClient().add_tags(node_id, current_user.ticket, added_tags)
        pp.pprint(add_tag_response)
        if add_tag_response.status_code == 201:
            flash('Keywords were successfully added to the file in the repository', 'success')
        elif add_tag_response.status_code == 403:
            flash('Could not add keywords to the file in the repository. Permission denied.', 'warning')
        else:
            flash('An unexpected error occurred while trying to add keywords to the file in the repository', 'danger')
        ############TAG ADDING###########

        data = {}

        data['node_id']                 = node_id
        data['title']                   = request_data.get('title')
        data['shortname']               = request_data.get('shortname')
        data['abstract']                = request_data.get('abstract') or None
        data['comments']                = request_data.get('comments') or None
        data['keywords']                = all_keywords
        data['start_date']              = datetime.strptime(request_data.get('start_date'), '%m/%d/%Y')
        data['end_date']                = datetime.strptime(request_data.get('end_date'), '%m/%d/%Y') if request_data.get('end_date') else None
        data['status_id']               = request_data.get('status')
        data['geographic_location']     = get_list([{ "northbound": request_data.get('northbound'),"southbound": request_data.get('southbound'),
                                            "eastbound": request_data.get('eastbound'), "westbound": request_data.get('westbound'),
                                            "description": request_data.get('geo_description')}])[0]
        data['methods']                 = request_data.get('methods') or None
        data['datatable']               = get_list(list(request_data['datatable'].values()))  if 'datatable' in request_data else None
        data['investigators']           = get_list(list(request_data['investigators'].values())) if 'investigators' in request_data else None
        data['personnel']               = get_list(list(request_data['personnel'].values())) if 'personnel' in request_data else None
        data['funding']                 = get_list(list(request_data['funding'].values())) if 'funding' in request_data else None

        # pp.pprint(data)

        metadata = CoreMetadata(**data)

        try:
            metadata.add_or_update()
        except Exception as e:
            print(e)
            flash('Metadata for file {} is already registered in the database.'.format(filename), 'danger')
        else:
            metadata.save()
            flash('Metadata for file {} was successfully registered in the database.'.format(filename), 'success')

        return redirect(url_for('.index'))

        # pp.pprint(request.form)

    js          = render_template('files/upload/wizard.js')
    tree        = UserFiles().shared_files_tree(whom=Who.all)
    keywords    = Keywords.taglist()
    statuses    = Status.select_list()
    form        = FileForm(keywords, statuses, data=None)
    return render_template('files/upload/wizard.html', user=current_user, title='Upload files', form=form.get_form(), tree=tree, js=js)

@mod_files.route('/create_folder', methods=['POST'])
@login_required
def create_folder():

    if request.method == 'POST':
        form = CreateFolderForm(request.form)
        if form.validate():

            request_data = request.form
            node_id = request_data['node_id']
            name = request_data['name']

            data = {}
            data['name'] = name
            data['nodeType'] = NodeType.folder.value

            create_folder_response = NodeClient().update_folder(node_id, current_user.ticket, data, Action.create_folder)

            if create_folder_response.status_code == 201:
                flash('The folder was created sucessfully.', 'success')
            else:
                flash('An unexpected error occurred while trying to create the folder', 'danger')

            return redirect(url_for('.index'))

@mod_files.route('/update_folder', methods=['POST', 'PUT'])
@login_required
def update_folder():

    if request.method == 'PUT':
        data = request.json
        name = data['name']
        node_id = data['node_id']
        body = {"name": name}
        update_folder_response = NodeClient().update_folder(node_id, current_user.ticket, body, Action.rename_folder)
        pp.pprint(update_folder_response)
        if update_folder_response.status_code == 200:
            flash('The item was renamed sucessfully.', 'success')
        elif update_folder_response.status_code == 403:
            flash('You don\'t have permission to update this item.', 'danger')
        elif update_folder_response.status_code == 404:
            flash('The parent folder does\'t exists.', 'danger')
        elif update_folder_response.status_code == 409:
            flash('Updated name clashes with an existing item in the current folder.', 'danger')
        elif update_folder_response.status_code == 409:
            flash('There was an integrity error in the request, possibly from invalid characters. Please try again.', 'danger')
        else:
            flash('An unexpected error occurred while trying to rename the item.', 'danger')
        return jsonify({"status_code": update_folder_response.status_code, "redirect_url": url_for('.index')})

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

@mod_files.route('/tags', methods=['GET'])
@login_required
def tags():
    _tags = ['csv', 'test']
    return jsonify(_tags)

@mod_files.route('/edit', methods=['GET', 'POST'])
@login_required
def edit():

    if request.method == 'POST':

        update = False
        metadata = None
        request_data = parse_multi_form(request.form)

        if 'metadata_id' in request_data:
            update = True
            metadata_id = request_data.pop('metadata_id')
            metadata = CoreMetadata.query.filter(CoreMetadata.id == metadata_id)

        node_id = request_data.pop('node_id')

        ############TAG ADDING###########
        all_keywords = request.form.getlist('keywords') + request_data.get('additional_keywords').split(',')
        added_tags = get_list([{"tag": keyword} for keyword in all_keywords])
        add_tag_response = NodeClient().add_tags(node_id, current_user.ticket, added_tags)
        if add_tag_response.status_code == 201:
            flash('Keywords for item with ID {} were successfully added to the file in the repository'.format(node_id), 'success')
        elif add_tag_response.status_code == 403:
            flash('Could not add keywords to the file in the repository. Permission denied.', 'warning')
        else:
            flash('An unexpected error occurred while trying to add keywords to the file in the repository', 'danger')
        ############TAG ADDING###########

        data = {}

        data['node_id']                 = node_id
        data['title']                   = request_data.get('title')
        data['shortname']               = request_data.get('shortname')
        data['abstract']                = request_data.get('abstract') or None
        data['comments']                = request_data.get('comments') or None
        data['keywords']                = all_keywords
        data['start_date']              = datetime.strptime(request_data.get('start_date'), '%m/%d/%Y')
        data['end_date']                = datetime.strptime(request_data.get('end_date'), '%m/%d/%Y') if request_data.get('end_date') else None
        data['status_id']               = request_data.get('status')
        data['geographic_location']     = get_list([{ "northbound": request_data.get('northbound'),"southbound": request_data.get('southbound'),
                                            "eastbound": request_data.get('eastbound'), "westbound": request_data.get('westbound'),
                                            "description": request_data.get('geo_description')}])[0]
        data['methods']                 = request_data.get('methods') or None
        data['datatable']               = get_list(list(request_data['datatable'].values()))  if 'datatable' in request_data else None
        data['investigators']           = get_list(list(request_data['investigators'].values())) if 'investigators' in request_data else None
        data['personnel']               = get_list(list(request_data['personnel'].values())) if 'personnel' in request_data else None
        data['funding']                 = get_list(list(request_data['funding'].values())) if 'funding' in request_data else None

        if metadata is None:
            metadata = CoreMetadata(**data)

        try:
            if update:
                metadata.update(data)
                db.session.commit()
                flash('Metadata for item with ID {} was successfully updated in the database.'.format(node_id), 'success')
            else:
                metadata.add_or_update()
                metadata.save()
                flash('Metadata for item with ID {} was successfully added to the database.'.format(node_id), 'success')
        except Exception as e:
            flash('There was an unexpected error when trying to update the metadata for \
                item with ID {} in the database.'.format(node_id), 'danger')

        return redirect(url_for('.index'))


    if 'id' in request.args:
        metadata_id = request.args.get('id')
        metadata = CoreMetadata.query.filter_by(id = metadata_id).first().serialize_form()
        js_data = {k: (metadata.pop(k) if metadata[k] else [{}]) for k in ('investigators', 'personnel', 'funding', 'datatable')}

        js          = render_template('files/edit/index.js', data=js_data)
        keywords    = Keywords.taglist()
        statuses    = Status.select_list()
        form        = FileForm(keywords, statuses, metadata)

        return render_template('files/edit/index.html', user=current_user, title='Edit metadata', form=form.get_form(), metadata_id=metadata_id, js=js)
    elif 'node_id' in request.args:
        node_id     = request.args.get('node_id')
        js          = render_template('files/edit/index.js')
        keywords    = Keywords.taglist()
        statuses    = Status.select_list()
        form        = FileForm(keywords, statuses, None)
        return render_template('files/edit/index.html', user=current_user, title='Edit metadata', form=form.get_form(), node_id=node_id, js=js)
    else:
        flash('No metadata ID or item ID specified in the request.', 'danger')
        return redirect(url_for('.index'))

@mod_files.route('/metadata', methods=['GET'])
@login_required
def metadata():
    # print('REQUEST: ', request)
    metadata_id = request.args.get('metadata_id')
    data = CoreMetadata.query.filter_by(id = metadata_id).first()

    _metadata = {"id": metadata_id, "data": data.serialize()}
    return jsonify(_metadata)
