from datetime import date
from typing import ClassVar, Literal

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..bases import Base, Data
from ..custom_types import (
    samplesheet_str,
    samplesheet_str_pk,
    stripped_str,
    stripped_str_pk,
)
from .entities import Lab, Person

PLATFORM_NAME = 'Xenium'


class Platform(Base, kw_only=True):
    __tablename__ = 'platform'

    # Platform attributes
    name: Mapped[stripped_str_pk]


class DataSet(Data, kw_only=True):
    __tablename__ = 'data_set'

    # DataSet attributes
    name: Mapped[samplesheet_str] = mapped_column(index=True)
    ilab_request_id: Mapped[stripped_str] = mapped_column(
        index=True
    )  # TODO: ilab request ID validation
    date_initialized: Mapped[date] = mapped_column(repr=False)

    # Parent foreign keys
    lab_id: Mapped[int] = mapped_column(ForeignKey('lab.id'), init=False, repr=False)
    platform_name: Mapped[str] = mapped_column(
        ForeignKey('platform.name'), default=PLATFORM_NAME, init=False
    )
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
    id_date_col: ClassVar[Literal['date_initialized']] = 'date_initialized'

    __mapper_args__ = {
        'polymorphic_on': 'platform_name',
    }

    def __post_init__(self):
        super().__post_init__()
        to_hash = (
            self.date_initialized,
            self.ilab_request_id,
            self.lab.pi.email,
            self.submitter.email,
            self.platform_name,
        )
        self.batch_id = hash(to_hash)


class Sample(Data, kw_only=True):
    __tablename__ = 'sample'

    # Sample attributes
    id: Mapped[samplesheet_str_pk]
    name: Mapped[samplesheet_str] = mapped_column(index=True)
    date_received: Mapped[date] = mapped_column(default_factory=date.today)

    # Parent foreign keys
    data_set_id: Mapped[int] = mapped_column(
        ForeignKey('data_set.id'), init=False, repr=False
    )
    platform_name: Mapped[str] = mapped_column(
        ForeignKey('platform.name'), default=PLATFORM_NAME, init=False
    )

    # Model metadata
    id_date_col: ClassVar[Literal['date_received']] = 'date_received'

    __mapper_args__ = {'polymorphic_on': 'platform_name'}
