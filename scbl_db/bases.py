from dataclasses import MISSING, Field, fields
from datetime import date
from re import fullmatch
from typing import ClassVar

from sqlalchemy.orm import DeclarativeBase, Mapped, MappedAsDataclass, mapped_column

from .custom_types import int_pk, samplesheet_str_pk, stripped_str_pk

__all__ = ['Base', 'Entity', 'Data', 'Process']


class Base(MappedAsDataclass, DeclarativeBase):
    @classmethod
    def dc_fields(cls) -> tuple[Field, ...]:
        return fields(cls)

    @classmethod
    def dc_init_fields(cls) -> tuple[Field, ...]:
        return tuple(f for f in cls.dc_fields() if f.init)

    @classmethod
    def required_dc_init_fields(cls) -> tuple[Field, ...]:
        return tuple(
            f
            for f in fields(cls)
            if f.init and f.default is MISSING and f.default_factory is MISSING
        )

    @classmethod
    def dc_field_names(cls) -> set[str]:
        return {f.name for f in cls.dc_fields()}

    @classmethod
    def dc_init_field_names(cls) -> set[str]:
        return {f.name for f in cls.dc_init_fields()}

    @classmethod
    def required_dc_init_field_names(cls) -> set[str]:
        return {f.name for f in cls.required_dc_init_fields()}

    pass


class Entity(Base, kw_only=True):
    __abstract__ = True


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

        if date_col is None:
            prefix = self.id_prefix
            suffix_length = self.id_length - len(self.id_prefix)
        else:
            year_last_two_digits = date_col.strftime('%y')
            year_last_two_digits_as_int = int(date_col.strftime('%y'))

            year_pattern = '|'.join(
                str(year_last_two_digits_as_int + i) for i in range(-1, 2)
            )

            prefix = self.id_prefix + f'({year_pattern})'
            suffix_length = (
                self.id_length - len(self.id_prefix) - len(year_last_two_digits)
            )

        pattern = rf'{prefix}\d{{{suffix_length}}}'

        model_name = type(self).__name__

        if fullmatch(pattern, self.id) is None:
            raise ValueError(
                f'{model_name} ID {self.id} does not match the pattern {pattern}.'
            )


class Process(Base, kw_only=True):
    __abstract__ = True

    name: Mapped[stripped_str_pk]
