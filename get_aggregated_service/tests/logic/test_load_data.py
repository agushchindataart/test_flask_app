"""Tests for logic.load_data module."""

from unittest.mock import Mock
from unittest.mock import mock_open
from unittest.mock import patch

import pytest

from get_aggregated_service.logic import load_data


@pytest.mark.parametrize(
    'field_name,field_value,expected_result',
    [
        ('country', 'ru', True),
        ('country', '2r32r', False),
        ('state', 'vrn', True),
        ('state', '123vrn123', False),
        ('city', 'Voronezh', True),
        ('city', 'V0ronezh', False),
        ('zip', '394000', True),
        ('zip', '394OOO', False),
        ('unknown', '1231231', False)
    ]
)
def test_check_address_field_all(field_name, field_value, expected_result):
    """Test for all possible address fields validations."""
    result = load_data._check_address_field(field_name, field_value)
    assert result == expected_result


def test_process_address_line_success():
    """Test for handling of correct address line."""
    address_line = 'country=us;city=newyork;state=ny;zip=10019'
    expected_result = {
        'country': 'us',
        'city': 'newyork',
        'state': 'ny',
        'zip': '10019'
    }

    result = load_data._process_address_line(address_line)
    assert result == expected_result


@pytest.mark.parametrize(
    'address_line',
    [
        'country=us;city=newyork;state=ny;zip=10019;key=value',
        'country=us;city=newyork;state=ny'
    ]
)
def test_process_address_line_wrong_field_count_failure(address_line):
    """Test for extra/missing address items."""
    result = load_data._process_address_line(address_line)
    assert result is None


@pytest.mark.parametrize(
    'address_line',
    [
        'country=us;city=newyork;state=ny;zip=10019=1231231',
        'country=us;city=newyork;state=ny;zip'
    ]
)
def test_process_address_line_broken_pair_failure(address_line):
    """Test for incorrect key=value address items."""
    result = load_data._process_address_line(address_line)
    assert result is None


def test_load_data_from_file_success():
    """Test for correct reading of data from file."""
    file_path = 'some/file/path.ext'
    file_content = """country=us;city=newyork;state=ny;zip=10019
country=ru;city=voronezh;state=vrn;zip=12313"""
    expected_result = [
        {
            'country': 'us',
            'city': 'newyork',
            'state': 'ny',
            'zip': '10019'
        },
        {
            'country': 'ru',
            'city': 'voronezh',
            'state': 'vrn',
            'zip': '12313'
        },
    ]
    with patch('builtins.open', mock_open(read_data=file_content)):
        result, message = load_data._load_data_from_file(file_path)
    assert result == expected_result


def test_load_data_from_file_skip_incorrect_address_line():
    """Test for skipping of lines with incorrect zip."""
    file_path = 'some/file/path.ext'
    file_content = """country=us;city=newyork;state=ny;zip=1ab19
country=ru;city=voronezh;state=vrn;zip=12313"""
    expected_result = [
        {
            'country': 'ru',
            'city': 'voronezh',
            'state': 'vrn',
            'zip': '12313'
        },
    ]
    with patch('builtins.open', mock_open(read_data=file_content)):
        result, message = load_data._load_data_from_file(file_path)
    assert result == expected_result


def test_load_data_from_file_raises_exception():
    """Test for skipping of lines with file open raising error."""
    file_path = 'some/file/path.ext'
    with patch('builtins.open') as exception_mock:
        exception_mock.side_effect = Exception('Some error')
        result, message = load_data._load_data_from_file(file_path)
    assert result is None
    assert message == (
        'Unknown error during processing of `some/file/path.ext`: `Some error`'
    )


@pytest.fixture
def file_1_load_result():
    """Return mock load data for file 1."""
    return [
        {
            'country': 'us',
            'city': 'newyork',
            'state': 'ny',
            'zip': '23424'
        }
    ]


@pytest.fixture
def file_2_load_result():
    """Return mock load data for file 2."""
    return [
        {
            'country': 'ru',
            'city': 'voronezh',
            'state': 'vrn',
            'zip': '3432'
        },
        {
            'country': 'ru',
            'city': 'voronezh',
            'state': 'vrn',
            'zip': '12313'
        },
    ]


@pytest.fixture
def file_3_load_result():
    """Return mock load data for file 3."""
    return [
        {
            'country': 'uk',
            'city': 'london',
            'state': 'lnd',
            'zip': '3123'
        },
    ]


def test_load_data_from_files_success(
        file_1_load_result, file_2_load_result, file_3_load_result):
    """Test for successful load from all files."""
    file_load_result_mock = Mock()
    file_load_result_mock.side_effect = [
        (file_1_load_result, ''),
        (file_2_load_result, ''),
        (file_3_load_result, ''),
    ]

    expected_result = (
            file_1_load_result + file_2_load_result + file_3_load_result)
    with patch('get_aggregated_service.logic.load_data._load_data_from_file',
               file_load_result_mock):
        result, message = load_data.load_data_from_files()
    assert result == expected_result


def test_load_data_from_files_single_file_load_faialure(
        file_1_load_result, file_3_load_result):
    """Test for failure in loading data from one of the files."""
    file_2_error_message = 'Some error message'
    file_load_result_mock = Mock()
    file_load_result_mock.side_effect = [
        (file_1_load_result, ''),
        (None, file_2_error_message),
        (file_3_load_result, ''),
    ]

    with patch('get_aggregated_service.logic.load_data._load_data_from_file',
               file_load_result_mock):
        result, message = load_data.load_data_from_files()
    assert result is None
    assert message == file_2_error_message
