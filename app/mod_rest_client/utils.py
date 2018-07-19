from flask_login import current_user
from flask import flash, redirect, url_for

def http_40x(message=None, category='danger', dest='auth.login'):
    try:
        current_user.logout()
    except Exception as e:
        raise e
    finally:
        flash(message, category)
        return redirect(url_for(dest))

def http_50x():
    pass