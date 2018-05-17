"""Main file of the service app. Contains handlers and runs app."""

from flask import Flask

from put_aggregated_service import config

app = Flask(__name__)
if config.LOGGER is not None:
    app.logger.addHandler(config.LOGGER)

from put_aggregated_service.handlers import *  # noqa


if __name__ == '__main__':
    debug = config.ENV == config.DEV_ENVIRONMENT
    app.run(config.PUT_SERVICE_HOST, config.PUT_SERVICE_PORT, debug=debug)
