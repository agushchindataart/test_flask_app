"""Tests for logic.format_data module."""

from xml.etree import ElementTree as ET

from get_aggregated_service.logic import format_data


def test_format_address_data_to_xml_success():
    """Test for generation of correct xml."""
    addresses = [
        {
            'country': 'us',
            'state': 'ny',
            'city': 'newyork',
            'zip': '1234325'
        },
        {
            'country': 'us',
            'state': 'nj',
            'city': 'newjersey',
            'zip': '23525'
        }
    ]

    result = format_data.format_address_data_to_xml(addresses)
    assert ET.fromstring(result)
