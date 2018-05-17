"""Main file of the service app. Contains handlers and runs app."""

import json

from flask import Flask
from flask import jsonify
from flask import Response

from get_aggregated_service import config
from get_aggregated_service.logic import format_data
from get_aggregated_service.logic import load_data

app = Flask(__name__)


@app.route('/health-check', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({'status': 'ok'})


@app.route('/get-address-data', methods=['GET'])
def get_aggregated_data():
    """Endpoint which reads, validates and returns address data as xml."""
    address_data, message = load_data.load_data_from_files()
    if address_data is None:
        return Response(
            response=json.dumps({'status': 'error', 'details': message}),
            status=500, mimetype='application/json')

    formatted_data = format_data.format_address_data_to_xml(address_data)
    return Response(formatted_data, mimetype='text/xml')


if __name__ == '__main__':
    app.run(config.GET_SERVICE_HOST, config.GET_SERVICE_PORT)
