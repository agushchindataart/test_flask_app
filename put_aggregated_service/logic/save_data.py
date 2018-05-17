"""Logic for data saving."""

import os

from put_aggregated_service import config
from put_aggregated_service.application import app


def save_data_to_file(address_data):
    """Save incoming data to file.

    Args:
        address_data(str): Address data formatted as XML.
    Return:
        tuple(bool, str): Return (True,'') if success, else (None, 'error_msg')

    """
    app.logger.info('Saving data to file')
    try:
        file_path = config.DESTINATION_FILE_PATH
        dir_path = os.path.dirname(file_path)

        # checking if destination folder exists
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        f = open(file_path, 'wb')
        f.write(address_data)
        f.close()
        app.logger.info('Saving success')
        return True, ''
    except IOError as e:
        error_tpl = 'IOError writing data to file `{file}`: `{error}`'
        error_msg = error_tpl.format(file=file_path, error=str(e))
        app.logger.error(error_msg)
        return None, error_msg
    except Exception as e:
        error_tpl = 'Unknown error writing data to file `{file}`: `{error}`'
        error_msg = error_tpl.format(file=file_path, error=str(e))
        app.logger.error(error_msg)
        return None, error_msg
