# Import flask dependencies
from flask import Blueprint, request, render_template, flash, redirect, url_for, abort, session
from jinja2 import TemplateNotFound
from flask_login import current_user, login_user, logout_user

from app.mod_auth.forms import LoginForm
from app.mod_auth.models import User
from app.mod_rest_client.client import AuthClient, PeopleClient

from app.mod_utils.utils import is_safe_url
from app import login

# Define the blueprint
mod_auth = Blueprint('auth', __name__)

@login.unauthorized_handler
def handle_needs_login():
    flash("You have to be logged in to access this page.", 'danger')
    return redirect(url_for('auth.login', next=request.endpoint))

@login.user_loader
def load_user(user_id):
    return User.query.get(user_id)

# Set the route and accepted methods
@mod_auth.route('/login/', methods=['GET', 'POST'])
def login():

    if current_user.is_authenticated:
        flash('User {} already authenticated'.format(current_user.email))
        return redirect(url_for('dashboard.index'))

    if request.method == 'POST':
        login_form = LoginForm()
        _next = request.args.get('next')
        if login_form.validate_on_submit():
            response = AuthClient().login(login_form.username.data, login_form.password.data)
            if response.status_code in [401, 403]:
                flash('Incorrect username or password', 'danger')
                return redirect(url_for('auth.login'))

            alf_ticket =  response.body['data']['ticket']
            user = User.query.filter_by(username=login_form.username.data).first()
            if user is None:
                user_response = PeopleClient().userinfo(login_form.username.data, alf_ticket)

                #Create a new user in local DB
                u = User(alf_ticket, **user_response.body)
                u.add_or_update()
                u.save()

                #Authenticate newly created user
                u.authenticate(alf_ticket)
                login_user(u)
            else:
                user.authenticate(alf_ticket)
                user.fetch_session_info()
                login_user(user)

            if not is_safe_url(_next):
                return abort(400)
            return redirect(url_for(_next) or url_for('dashboard.index'))

    login_form = LoginForm(formdata=None)
    return render_template('auth/login.html', title='Sign In', login_form=login_form)

@mod_auth.route('/logout/', methods=['GET'])
def logout():
    logout = AuthClient().logout(current_user.ticket)
    if logout.status_code == 200:
        current_user.logout()
        logout_user()
        flash('Logged out successfully.', 'success')
        return redirect(url_for('auth.login'))
