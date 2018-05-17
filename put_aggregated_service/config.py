"""Config file for put_aggregated service."""

import os

PUT_SERVICE_HOST = os.environ.get('PUT_SERVICE_HOST', '127.0.0.1')
PUT_SERVICE_PORT = os.environ.get('PUT_SERVICE_PORT', '5002')

DEV_ENVIRONMENT = 'dev'
TEST_ENVIRONMENT = 'test'
PROD_ENVIRONMENT = 'prod'

ENV = os.environ.get('ENV', DEV_ENVIRONMENT)

DESTINATION_FILE_PATH = os.path.join(
    os.path.dirname(__file__), 'data', 'address_data.xml')
