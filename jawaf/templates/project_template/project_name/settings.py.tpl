"""
jawaf settings for ${project_name} project.

Generated by 'jawaf-admin start-project' using jawaf ${version}.
"""

import os

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))

BASE_DIR = os.path.dirname(PROJECT_DIR)

PROJECT_NAME = '${project_name}'

TABLE_PREFIX = '${project_name}'

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '${secret_key}'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

INSTALLED_APPS = [
    'jawaf.auth',
]

AUTH_CONFIG = {
    'password_reset_expiration': 3, # Hours
    'database': 'default', # Specify the database jawaf.auth uses.
    'login_url': '/login/',
}

ROOT_ROUTE_CONF = '${project_name}.routes'

DATABASES = {
    'default': {
        'database': 'jawaf_${project_name}', # Default database name - change to match the database you want to use.
        'engine': 'postgresql',
        'host': 'localhost', # Set this to the host for your postgresql install, localhost by default.
        'port': '5432', # Port for your local install - typically 5432 or 5433
        'password': '', # Set this to the password for your postgresql install
        'user': '', # Set this to the user for your postgresql install
    }
}

SESSION = {
    'interface': 'memory', # Optionally use in memory for local development and testing
#    Use Redis for production, and also for local development and testing:
#    'host':'localhost',
#    'interface': 'redis',
#    'poolsize': 10,
#    'port': 6379,
}

HOST = '0.0.0.0'
PORT = 8000

TIME_ZONE = 'UTC'
