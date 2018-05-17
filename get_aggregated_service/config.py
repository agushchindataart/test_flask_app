"""Config file for get_aggregated service."""

import os

GET_SERVICE_HOST = os.environ.get('GET_SERVICE_HOST', '127.0.0.1')
GET_SERVICE_PORT = os.environ.get('GET_SERVICE_PORT', '5001')

PUT_SERVICE_HOST = os.environ.get('PUT_SERVICE_HOST', '127.0.0.1')
PUT_SERVICE_PORT = os.environ.get('PUT_SERVICE_PORT', '5002')

DEV_ENVIRONMENT = 'dev'
TEST_ENVIRONMENT = 'test'
PROD_ENVIRONMENT = 'prod'

ENV = os.environ.get('ENV', DEV_ENVIRONMENT)

SOURCE_FILES_DIR = os.path.join(os.path.dirname(__file__), 'data')

DEFAULT_SOURCE_FILES = (
    'File1.txt',
    'File2.txt',
    'File3.txt',
)

STRING_FIELDS = (
    'country',
    'state',
    'city',
)

NUMERIC_FIELDS = (
    'zip',
)
