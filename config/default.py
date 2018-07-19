import os

DEBUG = False
SECRET_KEY = os.environ.get('SECRET_KEY') or 'not-the-droid-youre-looking-for'

# Define the application directory
import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
