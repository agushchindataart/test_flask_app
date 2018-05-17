"""Contain method responsible for formatting output data."""

from xml.etree import ElementTree as ET


def format_address_data_to_xml(addresses):
    """Format given data to xml."""
    print(addresses)
    address_root = ET.Element('addresses')
    for address in addresses:
        address_node = ET.SubElement(address_root, 'address')
        for address_field, address_field_value in address.items():
            field_node = ET.SubElement(address_node, address_field)
            field_node.text = address_field_value
    result = ET.tostring(address_root).decode()

    return result
