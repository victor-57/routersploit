import unittest
import socket

try:
    import unittest.mock as mock
except ImportError:
    import mock

from routersploit.test import RoutersploitTestCase
from routersploit import validators
from routersploit.exceptions import OptionValidationError


class ValidatorsTest(RoutersploitTestCase):
    def test_url_adding_http_prefix(self):
        self.assertEqual(validators.url("127.0.0.1"), "http://127.0.0.1")

    def test_url_already_with_http_prefix(self):
        self.assertEqual(validators.url("http://127.0.0.1"), "http://127.0.0.1")

    def test_url_already_with_https_prefix(self):
        self.assertEqual(validators.url("https://127.0.0.1"), "https://127.0.0.1")

    def test_ipv4_valid_address(self):
        address = "127.0.0.1"
        self.assertEqual(validators.ipv4(address), address)

    def test_ipv4_invalid_address_1(self):
        """ IP address with segment out of range. """
        address = "127.256.0.1"
        with self.assertRaises(OptionValidationError):
            validators.ipv4(address)

    def test_ipv4_invalid_address_2(self):
        """ IP address with 4 digit segment. """
        address = "127.0.0.1234"
        with self.assertRaises(OptionValidationError):
            validators.ipv4(address)

    def test_ipv4_invalid_address_3(self):
        """ IP address with extra segment """
        address = "127.0.0.123.123"
        with self.assertRaises(OptionValidationError):
            validators.ipv4(address)

    @mock.patch("socket.inet_pton")
    def test_ipv4_no_inet_pton_valid_address(self, mock_inet_pton):
        address = "127.0.0.1"
        mock_inet_pton.side_effect = AttributeError
        self.assertEqual(validators.ipv4(address), "127.0.0.1")

    @mock.patch("socket.inet_pton")
    def test_ipv4_no_inet_pton_invalid_address_1(self, mock_inet_pton):
        """ IP address with segment out of range. """
        address = "127.256.0.1"
        mock_inet_pton.side_effect = AttributeError
        with self.assertRaises(OptionValidationError):
            validators.ipv4(address)

    @mock.patch("socket.inet_pton")
    def test_ipv4_no_inet_pton_invalid_address_2(self, mock_inet_pton):
        """ IP address with 4 digit segment. """
        address = "127.0.0.1234"
        mock_inet_pton.side_effect = AttributeError
        with self.assertRaises(OptionValidationError):
            validators.ipv4(address)

    @mock.patch("socket.inet_pton")
    def test_ipv4_no_inet_pton_invalid_address_3(self, mock_inet_pton):
        """ IP address with extra segment """
        address = "127.0.0.123.123"
        mock_inet_pton.side_effect = AttributeError
        with self.assertRaises(OptionValidationError):
            validators.ipv4(address)

    def test_ipv4_strip_scheme_1(self):
        address = "http://127.0.0.1"
        self.assertEqual(validators.ipv4(address), "127.0.0.1")

    def test_ipv4_strip_scheme_2(self):
        address = "ftp://127.0.0.1"
        self.assertEqual(validators.ipv4(address), "127.0.0.1")


if __name__ == '__main__':
    unittest.main()
