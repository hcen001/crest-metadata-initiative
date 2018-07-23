from app import db
from flask_login import current_user
from flask import flash, redirect, url_for

from app.mod_rest_client.client import NodeClient


class UserFiles(object):
    """docstring for UserFiles"""

    # def __init__(self):
    #     super(UserFiles, self).__init__()
    #     self.private_filelist = list()
    #     self.shared_filelist = list()

    @property
    def private_files(self):
        private_response = NodeClient().private_filelist(current_user.ticket)

        # if private_response.status_code in [401, 403]:
        #     current_user.logout()
        #     flash('Logged out due to inactivity. Please login again.', 'danger')
        #     return redirect(url_for('auth.login'))

        return private_response.body['list']['entries']

    @property
    def shared_files(self):
        shared_response = NodeClient().shared_filelist(current_user.ticket)

        # if shared_response.status_code in [401, 403]:
        #     current_user.logout()
        #     flash('Logged out due to inactivity. Please login again.', 'danger')
        #     return redirect(url_for('auth.login'))

        return shared_response.body['list']['entries']

    @property
    def shared_files_by_others(self):
        return [file for file in self.shared_files if current_user.username not in file['entry']['createdByUser'].values()]

    @property
    def shared_files_by_me(self):
        return [file for file in self.shared_files if current_user.username in file['entry']['createdByUser'].values()]

    @property
    def files(self):
        return self.private_files + self.shared_files