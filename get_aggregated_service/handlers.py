"""Get service handlers."""

import json

from flask import jsonify
from flask import Response

from get_aggregated_service.application import app
from get_aggregated_service.logic import format_data
from get_aggregated_service.logic import load_data


@app.route('/health-check', methods=['GET'])
def health_check():
    """Health check endpoint."""
    app.logger.info('Health check.')
    return jsonify({'status': 'ok'})


@app.route('/get-address-data', methods=['GET'])
def get_aggregated_data():
    """Endpoint which reads, validates and returns address data as xml."""
    app.logger.info('Get aggregated data.')
    address_data, message = load_data.load_data_from_files()
    if address_data is None:
        return Response(
            response=json.dumps({'status': 'error', 'details': message}),
            status=500, mimetype='application/json')

    formatted_data = format_data.format_address_data_to_xml(address_data)
    return Response(formatted_data, mimetype='text/xml')
