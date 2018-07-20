from flask import Blueprint, redirect, url_for, abort, render_template, flash
from flask_login import login_required, current_user

from app.mod_rest_client.client import NodeClient

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
    private_response = NodeClient().private_filelist(current_user.ticket)
    shared_response = NodeClient().shared_filelist(current_user.ticket)
    if private_response.status_code in [401, 403] or shared_response.status_code in [401, 403]:
        current_user.logout()
        flash('Logged out due to inactivity. Please login again.', 'danger')
        return redirect(url_for('auth.login'))

    private_files = private_response.body
    shared_files = shared_response.body

    stats = {}
    stats['private_files'] = len(private_files['list']['entries'])
    stats['shared_files'] = len(shared_files['list']['entries'])
    js = render_template('dashboard/index.js')
    return render_template('dashboard/index.html', user=current_user, stats=stats, title='Dashboard', js=js)