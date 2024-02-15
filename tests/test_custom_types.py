from re import sub
from string import punctuation, whitespace

from scbl_db.custom_types import SamplesheetString, StrippedString


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
            StrippedString().process_bind_param(string=string, dialect='')
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
        string = f'{illegal_punctuation}string{whitespace}string{illegal_punctuation}'

        assert (
            SamplesheetString().process_bind_param(string=string, dialect='')
            == 'string-string'
        )
