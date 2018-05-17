"""Handlers for put service."""

import json

from flask import jsonify
from flask import request
from flask import Response

from put_aggregated_service.application import app
from put_aggregated_service.logic import save_data


@app.route('/health-check', methods=['GET'])
def health_check():
    """Health check endpoint."""
    app.logger.info('Health check')
    return jsonify({'status': 'ok'})


@app.route('/put-address-data', methods=['PUT'])
def put_address_data():
    """Endpoint which receives and saves address data to file."""
    app.logger.info('Saving incoming data.')
    address_data = request.get_data()
    save_result, message = save_data.save_data_to_file(address_data)
    if save_result is None:
        return Response(
            response=json.dumps({'status': 'error', 'details': message}),
            status=500, mimetype='application/json')

    return Response(
        response=json.dumps({'status': 'ok'}),
        status=201, mimetype='application/json')
