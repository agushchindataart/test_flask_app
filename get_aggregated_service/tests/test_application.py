"""Test application handlers."""

from unittest.mock import patch

from get_aggregated_service.application import app


@patch('get_aggregated_service.logic.load_data.load_data_from_files')
@patch('get_aggregated_service.logic.format_data.format_address_data_to_xml')
def test_get_addresses_data_success(format_data_mock, load_data_mock):
    """Test for success of endpoint."""
    format_data_mock.return_value = '<addresses></addresses>'
    load_data_mock.return_value = [], ''
    test_client = app.test_client()

    result = test_client.get('/get-address-data')
    assert result._status_code == 200


@patch('get_aggregated_service.logic.load_data.load_data_from_files')
@patch('get_aggregated_service.logic.format_data.format_address_data_to_xml')
def test_get_addresses_data_failure(format_data_mock, load_data_mock):
    """Test for failure of endpoint in getting load data."""
    format_data_mock.return_value = '<addresses></addresses>'
    load_data_mock.return_value = None, ''
    test_client = app.test_client()

    result = test_client.get('/get-address-data')
    assert result._status_code == 500
