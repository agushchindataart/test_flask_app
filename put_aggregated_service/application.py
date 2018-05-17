"""Main file of the service app. Contains handlers and runs app."""

import json

from flask import Flask
from flask import jsonify
from flask import request
from flask import Response

from put_aggregated_service import config
from put_aggregated_service.logic import save_data

app = Flask(__name__)


@app.route('/health-check', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({'status': 'ok'})


@app.route('/put-address-data', methods=['PUT'])
def put_address_data():
    """Endpoint which receives and saves address data to file."""
    address_data = request.get_data()
    save_result, message = save_data.save_data_to_file(address_data)
    if save_result is None:
        return Response(
            response=json.dumps({'status': 'error', 'details': message}),
            status=500, mimetype='application/json')

    return Response(
        response=json.dumps({'status': 'ok'}),
        status=201, mimetype='application/json')


if __name__ == '__main__':
    app.run(config.PUT_SERVICE_HOST, config.PUT_SERVICE_PORT)
