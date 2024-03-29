from re import sub
from string import ascii_letters, digits
from typing import Annotated

from sqlalchemy.orm import mapped_column
from sqlalchemy.types import Integer, String, TypeDecorator


class StrippedString(TypeDecorator):
    """
    A string type that strips whitespace from the ends of the string
    before sending to the database.
    """

    impl = String
    cache_ok = True

    def process_bind_param(self, string, dialect) -> str | None:
        return string.strip() if isinstance(string, str) else string


class SamplesheetString(TypeDecorator):
    """
    A string type that removes illegal characters from the string before
    sending to the database. Suitable for strings that will be used in
    the samplesheet passed as input to the `nf-tenx` pipeline.
    """

    impl = String
    cache_ok = True

    def process_bind_param(self, string: str | None, dialect) -> str | None:
        if not isinstance(string, str):
            return string

        sep_chars = r'\s_-'
        sep_chars_group = r'[\s_-]'
        samplesheet_blacklist_pattern = rf'[^{ascii_letters + digits + sep_chars}]'

        # Remove illegal characters
        string = sub(
            pattern=samplesheet_blacklist_pattern, repl='', string=string.strip()
        )

        # Replace separator characters with hyphens
        string = sub(pattern=sep_chars_group, repl='-', string=string)

        # Replace occurrences of multiple hyphens with a single hyphen
        string = sub(pattern=r'-+', repl='-', string=string)

        return string


# TODO these should just be encoded as str
# class XeniumSlideSerialNumber(TypeDecorator):
#     """ """

#     impl = Integer
#     cache_ok = True

#     def process_bind_param(self, serial_number, dialect) -> int:
#         return (
#             int(serial_number.strip())
#             if isinstance(serial_number, str)
#             else serial_number
#         )

#     def process_result_value(self, serial_number, dialect) -> str:
#         return (
#             f'{serial_number:07}' if isinstance(serial_number, int) else serial_number
#         )


# Commonly used primary key types
int_pk = Annotated[int, mapped_column(primary_key=True)]
stripped_str_pk = Annotated[str, mapped_column(StrippedString, primary_key=True)]
samplesheet_str_pk = Annotated[str, mapped_column(SamplesheetString, primary_key=True)]

# Commonly used non-unique string types
stripped_str = Annotated[str, mapped_column(StrippedString)]
samplesheet_str = Annotated[str, mapped_column(SamplesheetString)]

# Commonly used unique types
unique_int = Annotated[int, mapped_column(unique=True)]
unique_stripped_str = Annotated[str, mapped_column(StrippedString, unique=True)]
unique_samplesheet_str = Annotated[str, mapped_column(SamplesheetString, unique=True)]
# xenium_slide_serial_number = Annotated[
#     str, mapped_column(XeniumSlideSerialNumber, unique=True)
# ]
