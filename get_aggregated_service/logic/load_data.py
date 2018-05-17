"""Contain logic related to reading and validating of address data."""

import os

from get_aggregated_service import config
from get_aggregated_service.application import app

logger = app.logger


def _check_address_field(address_field, address_field_value):
    """Check if address field format is correct.

    Args:
        address_field (str): Name of address field.
        address_field_value (str): Value of address field.

    Returns:
        bool: True if format is correct, else False.

    """
    if address_field in config.STRING_FIELDS:
        check_result = address_field_value.isalpha()
        if not check_result:
            error_tpl = 'Field `{field}` must be string, its value `{value}`'
    elif address_field in config.NUMERIC_FIELDS:
        check_result = address_field_value.isdigit()
        if not check_result:
            error_tpl = 'Field `{field}` must be numeric, its value `{value}`'
    else:
        check_result = False
        error_tpl = 'Unknown address field `{field}` with value `{value}`'

    if not check_result:
        error_msg = error_tpl.format(
            field=address_field, value=address_field_value)
        logger.error(error_msg)
    return check_result


def _process_address_line(address_line):
    """Process address line.

    Args:
        address_line (str): Address line from csv file.

    Returns:
        dict: Address data dict if line is correct.

    """
    address_items = address_line.split(';')
    result = {}

    # checking if address contains from 4 parts separated by '='
    if len(address_items) == 4:
        for address_item in address_items:
            address_item_split = address_item.split('=')
            if len(address_item_split) != 2:
                error_tpl = 'Incorrect address item: {item}'
                error_msg = error_tpl.format(item=address_item)
                logger.error(error_msg)
                return None
            address_field, address_field_value = address_item_split
            item_check_result = _check_address_field(
                address_field, address_field_value)
            if item_check_result:
                result[address_field] = address_field_value
            else:
                return None
        return result
    else:
        error_tpl = 'Incorrect address line: `{line}`. Too many items'
        error_msg = error_tpl.format(line=address_line)
        logger.error(error_msg)
        return None


def _load_data_from_file(full_file_path):
    """Process file.

    Args:
        full_file_path (str): Absolute path to file.

    Returns:
        list: List of correct file addresses.

    """
    logger.info('Processing file {file}'.format(file=full_file_path))

    result = []
    try:
        f = open(full_file_path)
        address_lines = f.read().splitlines()
        for address_line in address_lines:
            address_line_check_result = _process_address_line(address_line)
            if address_line_check_result is None:
                error_tpl = 'Skipping line `{line}` for file `{file}`'
                error_msg = error_tpl.format(
                    line=address_line, file=full_file_path)
                logger.error(error_msg)
            else:
                result.append(address_line_check_result)
        f.close()

    except IOError as e:
        error_tpl = 'IOError opening `{file}`: `{error}`'
        error_msg = error_tpl.format(file=full_file_path, error=str(e))
        logger.error(error_msg)
        return None, error_msg
    except Exception as e:
        error_tpl = 'Unknown error during processing of `{file}`: `{error}`'
        error_msg = error_tpl.format(file=full_file_path, error=str(e))
        logger.error(error_msg)
        return None, error_msg

    logger.info('Processing file {file} finished'.format(file=full_file_path))
    return result, ''


def load_data_from_files():
    """Load data from files listed in app config.

    Returns:
        list: List of address records from all files.

    """
    logger.info('Loading data from files.')
    files_storage_path = config.SOURCE_FILES_DIR
    file_names = config.DEFAULT_SOURCE_FILES
    result = []

    # processing files one by one
    for file_name in file_names:
        full_file_path = os.path.join(files_storage_path, file_name)
        load_from_file_result, message = _load_data_from_file(full_file_path)
        if load_from_file_result is None:
            return None, message
        else:
            result.extend(load_from_file_result)

    logger.info('Loading data from files finished.')

    return result, ''
