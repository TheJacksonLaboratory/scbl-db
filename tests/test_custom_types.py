from re import sub
from string import punctuation, whitespace

from pytest import raises

from scbl_db.custom_types import (
    SamplesheetString,
    StrippedString,
    XeniumSlideSerialNumber,
)


class TestStrippedString:
    """
    Tests for the `StrippedString` type.
    """

    def test_process_bind_param(self):
        """
        Test that the `process_bind_param` method strips whitespace from
        the ends of the string but does not modify the string otherwise.
        """
        string = f'{whitespace}{punctuation}string{punctuation}{whitespace}'

        assert (
            StrippedString().process_bind_param(string=string, dialect=None)
            == f'{punctuation}string{punctuation}'
        )


class TestSamplesheetString:
    """
    Tests for the `SamplesheetString` type.
    """

    def test_process_bind_param(self):
        """
        Test that the `process_bind_param` method removes illegal
        characters from the string.
        """
        illegal_punctuation = sub(pattern='[-_]', repl='', string=punctuation)
        if illegal_punctuation != punctuation.replace('-', '').replace('_', ''):
            raise ValueError(
                'Hyphen (-) and underscore (_) not removed correctly from punctuation.'
            )

        string = f'{illegal_punctuation}string{whitespace}string{illegal_punctuation}'

        assert (
            SamplesheetString().process_bind_param(string=string, dialect=None)
            == 'string-string'
        )


class TestXeniumSlideSerialNumber:
    """
    Tests for the `XeniumSlideSerialNumber` type.
    """

    serial_number_as_int = 99999

    def test_process_bind_param(self):
        """
        Test that the `process_bind_param` method strips whitespace from
        the ends of the string and casts the string to an integer.
        """
        serial_number = f'{whitespace}00{self.serial_number_as_int}{whitespace}'

        assert (
            XeniumSlideSerialNumber().process_bind_param(serial_number, dialect=None)
            == self.serial_number_as_int
        )

    def test_process_invalid_bind_param(self):
        """
        Test that the `process_bind_param` method raises an error if the
        string is not a valid integer.
        """
        serial_number = 'string'

        with raises(ValueError):
            XeniumSlideSerialNumber().process_bind_param(serial_number, dialect=None)

    def test_process_result_value(self):
        """
        Test that the `process_result_value` method casts the integer to a
        string and pads it with a leading zero if it is a single digit.
        """
        assert (
            XeniumSlideSerialNumber().process_result_value(
                self.serial_number_as_int, dialect=None
            )
            == f'00{self.serial_number_as_int}'
        )
