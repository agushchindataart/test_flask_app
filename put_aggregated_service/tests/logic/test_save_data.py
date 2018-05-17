"""Test logic.save_data module."""

import os
from unittest.mock import mock_open
from unittest.mock import patch

from put_aggregated_service import config
from put_aggregated_service.logic import save_data


@patch('os.path.exists')
def test_save_data_to_file_success(exists_mock):
    """Test for successful saving to file."""
    exists_mock.return_value = True
    data = '<addresses></addresses>'

    with patch('builtins.open', mock_open()) as file_mock:
        result, message = save_data.save_data_to_file(data)

    file_mock.assert_called_once_with(config.DESTINATION_FILE_PATH, 'wb')
    write_handler = file_mock()
    write_handler.write.assert_called_once_with(data)

    assert result is True


@patch('os.path.exists')
@patch('os.makedirs')
def test_save_data_to_file_dir_creation_success(makedirs_mock, exists_mock):
    """Test for successful saving to file with path creation."""
    exists_mock.return_value = False
    data = '<addresses></addresses>'

    with patch('builtins.open', mock_open()) as file_mock:
        result, message = save_data.save_data_to_file(data)

    file_mock.assert_called_once_with(config.DESTINATION_FILE_PATH, 'wb')
    write_handler = file_mock()
    write_handler.write.assert_called_once_with(data)
    makedirs_mock.assert_called_once_with(
        os.path.dirname(config.DESTINATION_FILE_PATH))

    assert result is True


@patch('os.path.exists')
def test_save_data_to_file_io_error_failure(exists_mock):
    """Test for failure with IO error."""
    exists_mock.return_value = True
    data = '<addresses></addresses>'
    io_error_message = 'Some IO error'
    with patch('builtins.open', mock_open()) as exception_file_mock:
        exception_file_mock.side_effect = IOError(io_error_message)
        result, message = save_data.save_data_to_file(data)

    exception_file_mock.assert_called_once_with(
        config.DESTINATION_FILE_PATH, 'wb')

    assert result is None
    assert message == (
        'IOError writing data to file `{file_path}`: `{error}`'.format(
            file_path=config.DESTINATION_FILE_PATH, error=io_error_message))
