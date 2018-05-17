"""Contain logic related to reading and validating of address data."""

import os

from get_aggregated_service import config


def _check_address_field(address_field, address_field_value):
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
        print(error_msg)
    return check_result


def _process_address_line(address_line):
    address_items = address_line.split(';')
    result = {}
    if len(address_items) == 4:
        for address_item in address_items:
            address_item_split = address_item.split('=')
            if len(address_item_split) != 2:
                error_tpl = 'Incorrect address item: {item}'
                error_msg = error_tpl.format(item=address_item)
                print(error_msg)
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
        print(error_msg)
        return None


def _load_data_from_file(full_file_path):
    print('Processing file {file}'.format(file=full_file_path))
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
                print(error_msg)
            else:
                result.append(address_line_check_result)
        return result, ''
    except IOError as e:
        error_tpl = 'IOError opening `{file}`: `{error}`'
        error_msg = error_tpl.format(file=full_file_path, error=str(e))
        return None, error_msg
    except Exception as e:
        error_tpl = 'Unknown error during processing of `{file}`: `{error}`'
        error_msg = error_tpl.format(file=full_file_path, error=str(e))
        print(error_msg)
        return None, error_msg


def load_data_from_files():
    """Load data from files listed in app config."""
    files_storage_path = config.SOURCE_FILES_DIR
    file_names = config.DEFAULT_SOURCE_FILES
    result = []
    for file_name in file_names:
        full_file_path = os.path.join(files_storage_path, file_name)
        load_from_file_result, message = _load_data_from_file(full_file_path)
        if load_from_file_result is None:
            return None, message
        else:
            result.extend(load_from_file_result)

    return result, ''
