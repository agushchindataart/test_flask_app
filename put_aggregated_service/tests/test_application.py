"""Test application handlers."""

from unittest.mock import patch

from put_aggregated_service.application import app


@patch('put_aggregated_service.logic.save_data.save_data_to_file')
def test_put_addresses_data_success(save_data_mock):
    """Test for success of endpoint."""
    data = '<addresses></addresses>'
    save_data_mock.return_value = True, ''

    test_client = app.test_client()
    result = test_client.put('/put-address-data', data=data)

    save_data_mock.assert_called_once_with(b'<addresses></addresses>')
    assert result._status_code == 201


@patch('put_aggregated_service.logic.save_data.save_data_to_file')
def test_put_addresses_data_failure(save_data_mock):
    """Test for failure of endpoint in saving load data."""
    save_data_mock.return_value = None, ''
    test_client = app.test_client()

    result = test_client.put('/put-address-data')
    assert result._status_code == 500
