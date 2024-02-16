from dataclasses import field
from datetime import date
from re import fullmatch
from typing import ClassVar

from sqlalchemy import ForeignKey
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates

from ..base import Base
from ..custom_types import (
    SamplesheetString,
    samplesheet_str,
    samplesheet_str_pk,
    stripped_str,
    stripped_str_pk,
)
from .entities import Lab, Person


class Platform(Base, kw_only=True):
    __tablename__ = 'platform'

    # Platform attributes
    name: Mapped[stripped_str_pk]
    # data_set_id_prefix: Mapped[str] = mapped_column(SamplesheetString(length=2))
    # sample_id_prefix: Mapped[str] = mapped_column(SamplesheetString(length=2))
    # data_set_id_length: Mapped[int]
    # sample_id_length: Mapped[int]

    # @validates('data_set_id_prefix', 'sample_id_prefix')
    # def validate_prefix(self, key: str, prefix: str) -> str:
    #     pattern = r'^[A-Z]{2}$'
    #     prefix = prefix.upper().strip()

    #     if fullmatch(pattern, prefix) is None:
    #         raise ValueError(
    #             f'{key} {prefix} does not match the pattern {pattern}.'
    #         )

    #     return prefix

    # @validates('data_set_id_length', 'sample_id_length')
    # def validate_id_length(self, key: str, id_length: int) -> int:
    #     min_id_length = 7
    #     max_id_length = 9

    #     if not min_id_length <= id_length <= max_id_length:
    #         raise ValueError(
    #             f'{key} must be between {min_id_length} and {max_id_length}, but {id_length} was given.'
    #         )

    #     return id_length

    # @property
    # def prefixes(self) -> dict[str, str]:
    #     return {'DataSet': self.data_set_id_prefix, 'Sample': self.sample_id_prefix}

    # @property
    # def id_lengths(self) -> dict[str, int]:
    #     return {'DataSet': self.data_set_id_length, 'Sample': self.sample_id_length}


class DataSet(Base, kw_only=True):
    __tablename__ = 'data_set'

    # DataSet attributes
    # TODO: auto-incrementing behavior
    id: Mapped[samplesheet_str_pk]
    name: Mapped[samplesheet_str] = mapped_column(index=True)
    ilab_request_id: Mapped[stripped_str] = mapped_column(
        index=True
    )  # TODO: ilab request ID validation
    date_initialized: Mapped[date] = mapped_column(repr=False)

    # Parent foreign keys
    lab_id: Mapped[int] = mapped_column(ForeignKey('lab.id'), init=False, repr=False)
    platform_name: Mapped[str] = mapped_column(ForeignKey('platform.name'))
    submitter_id: Mapped[int] = mapped_column(
        ForeignKey('person.id'), init=False, repr=False
    )

    # Parent models
    lab: Mapped[Lab] = relationship()
    platform: Mapped[Platform] = relationship(init=False, repr=False)
    submitter: Mapped[Person] = relationship()

    # Automatically set attributes
    batch_id: Mapped[int] = mapped_column(init=False, default=None, repr=False)

    # Model metadata
    id_based_on: ClassVar[str] = 'date_initialized'
    id_prefix: ClassVar[str | None] = None
    id_length: ClassVar[int | None] = None

    __mapper_args__ = {
        'polymorphic_on': 'platform_name',
    }

    @validates('id')
    def validate_id(self, key: str, id: str) -> str | None:
        if self.id_prefix is None or self.id_length is None:
            return

        id = id.strip().upper()
        pattern = rf'{self.id_prefix}\d{self.id_length - 2}'

        if fullmatch(pattern, id) is None:
            raise ValueError(f'{key} {id} does not match the pattern {pattern}.')

        return id

    def __post_init__(self):
        to_hash = (
            self.date_initialized,
            self.ilab_request_id,
            self.lab.pi.email,
            self.submitter.email,
            self.platform_name,
        )
        self.batch_id = hash(to_hash)


class Sample(Base, kw_only=True):
    __tablename__ = 'sample'

    # Sample attributes
    id: Mapped[samplesheet_str_pk]
    name: Mapped[samplesheet_str] = mapped_column(index=True)
    date_received: Mapped[date] = mapped_column(default_factory=date.today)

    # Parent foreign keys
    data_set_id: Mapped[int] = mapped_column(
        ForeignKey('data_set.id'), init=False, repr=False
    )
    platform_name: Mapped[str] = mapped_column(ForeignKey('platform.name'), init=False)

    # Model metadata
    id_based_on: ClassVar[str] = 'date_received'
    id_prefix: ClassVar[str | None] = None
    id_length: ClassVar[int | None] = None

    __mapper_args__ = {'polymorphic_on': 'platform_name'}

    @validates('id')
    def validate_id(self, key: str, id: str) -> str | None:
        if self.id_prefix is None or self.id_length is None:
            return

        id = id.strip().upper()
        pattern = rf'{self.id_prefix}\d{self.id_length - 2}'

        if fullmatch(pattern, id) is None:
            raise ValueError(f'{key} {id} does not match the pattern {pattern}.')

        return id
