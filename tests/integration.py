"""Simple end-to-end test for get_aggregated and put_aggregated services."""

import os

from urllib import request

from get_aggregated_service import config as get_config
from put_aggregated_service import config as put_config

get_url = 'http://{host}:{port}/get-address-data'.format(
    host=get_config.GET_SERVICE_HOST, port=get_config.GET_SERVICE_PORT)

put_url = 'http://{host}:{port}/put-address-data'.format(
    host=put_config.PUT_SERVICE_HOST, port=put_config.PUT_SERVICE_PORT)

if os.path.exists(put_config.DESTINATION_FILE_PATH):
    os.remove(put_config.DESTINATION_FILE_PATH)

with request.urlopen(get_url) as f:
    address_data = f.read().decode()

assert f.status == 200

req = request.Request(url=put_url, data=address_data.encode(), method='PUT')
with request.urlopen(req) as f:
    pass

assert f.status == 201
assert os.path.exists(put_config.DESTINATION_FILE_PATH)
destination_data = open(put_config.DESTINATION_FILE_PATH).read()

assert address_data == destination_data


