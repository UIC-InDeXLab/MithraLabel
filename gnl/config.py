"""
gnl development configuration.
"""

import os

# Root of this application, useful if it doesn't occupy an entire domain
APPLICATION_ROOT = '/'

# Secret key for encrypting cookies
SECRET_KEY = b'\x90\xf4M\x16\xaa2\xa1\xe5\x18\x01\xc3\xc8n\xdb\xbd\xb8\x94vSf\x1a\xc4c\x8d'  # noqa: E501  pylint: disable=line-too-long
# SESSION_COOKIE_NAME = 'login'

# File Upload to var/uploads/
UPLOAD_FOLDER = os.path.join(
    os.path.dirname(os.path.dirname(os.path.realpath(__file__))),
    'var', 'uploads'
)

DATA_FOLDER = os.path.join(
    os.path.dirname(os.path.dirname(os.path.realpath(__file__))),
    'gnl','static','data'
)


COVERAGE_FOLDER = os.path.join(
    os.path.dirname(os.path.dirname(os.path.realpath(__file__))),
    'CoverageJava'
)
CURRENT_FILE = None
CURRENT_TEMP_FILE = os.path.join(
    UPLOAD_FOLDER, 'tempdata.csv'
)
NUM_MISSING=0
OUTPUT=None
MUPS=None
CURRENT_DF=None
JSON_OUT={}
CURRENT_DF_NAMES_DICT_WITH_IGNORED={}
CURRENT_MANUAL_INFO={}
CURRENT_IGNORED_COLUMNS=[]
CURRENT_SELECTION={}
CURRENT_COLUMN_TYPES=None
CURRENT_DF_WITH_IGNORED_COLUMNS=None
CURRENT_LOADED=False

PRELOADED=False

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif', 'cvs'])

# 1 GB
MAX_CONTENT_LENGTH = 1024  * 1024 * 1024

# Database file is var/gnl.sqlite3
DATABASE_FILENAME = os.path.join(
    os.path.dirname(os.path.dirname(os.path.realpath(__file__))),
    'var', 'gnl.sqlite3'
)
