from datetime import date
from re import fullmatch
from typing import ClassVar

from sqlalchemy import inspect
from sqlalchemy.orm import DeclarativeBase, Mapped, MappedAsDataclass, mapped_column

from .custom_types import int_pk, samplesheet_str_pk


class Base(MappedAsDataclass, DeclarativeBase):
    pass


class Entity(Base, kw_only=True):
    __abstract__ = True

    id: Mapped[int_pk] = mapped_column(init=False, repr=False, compare=False)


class Data(Base, kw_only=True):
    __abstract__ = True

    # TODO: auto incrementing behavior
    id: Mapped[samplesheet_str_pk]

    # Model metadata
    id_date_col: ClassVar[str]
    id_prefix: ClassVar[str]
    id_length: ClassVar[int]

    def __post_init__(self):
        self.id = self.id.strip().upper()

        date_col: date = getattr(self, self.id_date_col)
        year_last_two_digits = date_col.strftime('%y')

        prefix = self.id_prefix + year_last_two_digits
        suffix_length = self.id_length - len(prefix)
        pattern = rf'{prefix}\d{{{suffix_length}}}'

        model_name = type(self).__name__

        if fullmatch(pattern, self.id) is None:
            raise ValueError(
                f'{model_name} ID {self.id} does not match the pattern {pattern}.'
            )