import os
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Connect to the database

# TODO IMPLEMENT DATABASE URL
SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:toor@localhost:5432/fyyur'

# Disable Warning
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Change templates on the fly
TEMPLATES_AUTO_RELOAD = True