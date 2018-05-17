"""Main file of the service app."""

from flask import Flask

from get_aggregated_service import config

app = Flask(__name__)
if config.LOGGER is not None:
    app.logger.addHandler(config.LOGGER)

from get_aggregated_service.handlers import *  # noqa

if __name__ == '__main__':
    app.run(config.GET_SERVICE_HOST, config.GET_SERVICE_PORT)
