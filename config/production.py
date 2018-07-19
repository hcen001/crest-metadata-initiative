import os

DEBUG = False
SECRET_KEY = os.environ.get('SECRET_KEY') or 'not-the-droid-youre-looking-for'
