"""Config file for get_aggregated service."""

import logging
from logging.handlers import RotatingFileHandler
import os

GET_SERVICE_HOST = os.environ.get('GET_SERVICE_HOST', '127.0.0.1')
GET_SERVICE_PORT = os.environ.get('GET_SERVICE_PORT', '5001')

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

LOGS_PATH = os.path.join(
    os.path.dirname(__file__), 'logs', 'get_service.log')

formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

LOGGER = None
if ENV == PROD_ENVIRONMENT:
    logs_path = LOGS_PATH
    logs_path_dir = os.path.dirname(logs_path)
    if not os.path.exists(logs_path_dir):
        os.makedirs(logs_path_dir)

    rotating_log_handler = RotatingFileHandler(
        LOGS_PATH, maxBytes=1024 * 1024, backupCount=3)
    rotating_log_handler.setLevel(logging.ERROR)
    rotating_log_handler.setFormatter(formatter)
    LOGGER = rotating_log_handler
