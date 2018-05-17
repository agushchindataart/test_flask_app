"""Logic for data saving."""

import os

from put_aggregated_service import config


def save_data_to_file(address_data):
    """Save incoming data to file."""
    try:
        file_path = config.DESTINATION_FILE_PATH
        dir_path = os.path.dirname(file_path)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        f = open(file_path, 'wb')
        f.write(address_data)
        f.close()
        return True, ''
    except IOError as e:
        error_tpl = 'IOError writing data to file `{file}`: `{error}`'
        error_msg = error_tpl.format(file=file_path, error=str(e))
        print(error_msg)
        return None, error_msg
    except Exception as e:
        error_tpl = 'Unknown error writing data to file `{file}`: `{error}`'
        error_msg = error_tpl.format(file=file_path, error=str(e))
        print(error_msg)
        return None, error_msg
