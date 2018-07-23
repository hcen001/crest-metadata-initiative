from flask import Blueprint, redirect, url_for, abort, render_template, flash
from flask_login import login_required, current_user

from app.mod_rest_client.client import NodeClient
from app.mod_dashboard.models import UserFiles

import pprint

# Define the blueprint
entry_point = Blueprint('dashboard', __name__)

# Set the route and accepted methods
@entry_point.route('/', methods=['GET'])
def index():
    try:
        return redirect(url_for('dashboard.dashboard'))
    except Exception as e:
        raise e
        abort(404)

@entry_point.route('/dashboard', methods=['GET'])
@login_required
def dashboard():

    pp = pprint.PrettyPrinter(indent=2)

    userfiles = UserFiles()

    stats = {}
    stats['private_files'] = len(userfiles.private_files)
    stats['shared_files_by_me'] = len(userfiles.shared_files_by_me)
    stats['shared_files_by_others'] = len(userfiles.shared_files_by_others)

    js = render_template('dashboard/index.js')
    return render_template('dashboard/index.html', user=current_user, stats=stats, title='Dashboard', js=js)