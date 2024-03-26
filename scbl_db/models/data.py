from datetime import date
from typing import ClassVar, Literal

from sqlalchemy import ForeignKey, ForeignKeyConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates

from ..bases import Base, Data
from ..custom_types import samplesheet_str, stripped_str
from .entities import Lab, Person
from .processes import Assay

__all__ = ['DataSet', 'Sample']


class DataSet(Data, kw_only=True):
    __tablename__ = 'data_set'

    # DataSet attributes
    # TODO: ilab request ID validation
    ilab_request_id: Mapped[stripped_str] = mapped_column(index=True, repr=False)
    date_initialized: Mapped[date] = mapped_column(repr=False)

    # Parent foreign keys
    assay_name: Mapped[str] = mapped_column(
        ForeignKey('assay.name'), init=False, repr=False
    )
    lab_name: Mapped[str] = mapped_column(init=False, repr=False)
    lab_pi_email: Mapped[str] = mapped_column(init=False, repr=False)
    lab_institution_name: Mapped[str] = mapped_column(init=False, repr=False)
    platform_name: Mapped[str] = mapped_column(
        ForeignKey('platform.name'), init=False, repr=False
    )
    submitter_email: Mapped[str] = mapped_column(
        ForeignKey('person.email'), init=False, repr=False
    )

    # Parent models
    assay: Mapped[Assay] = relationship(repr=False)
    lab: Mapped[Lab] = relationship(repr=False)
    submitter: Mapped[Person] = relationship(repr=False)

    # Model metadata
    id_date_col: ClassVar[Literal['date_initialized']] = 'date_initialized'

    __mapper_args__ = {
        'polymorphic_on': 'platform_name',
    }

    __table_args__ = (
        ForeignKeyConstraint(
            columns=['lab_name', 'lab_pi_email', 'lab_institution_name'],
            refcolumns=['lab.name', 'lab.pi_email', 'lab.institution_name'],
        ),
    )


class Sample(Data, kw_only=True):
    __tablename__ = 'sample'

    # Sample attributes
    name: Mapped[samplesheet_str] = mapped_column(index=True)
    date_received: Mapped[date] = mapped_column(repr=False)

    # Parent foreign keys
    data_set_id: Mapped[str] = mapped_column(
        ForeignKey('data_set.id'), default=None, init=False, repr=False
    )
    platform_name: Mapped[str] = mapped_column(
        ForeignKey('platform.name'), init=False, repr=False
    )

    # Model metadata
    id_date_col: ClassVar[Literal['date_received']] = 'date_received'

    __mapper_args__ = {'polymorphic_on': 'platform_name'}
