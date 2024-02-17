from datetime import date
from typing import ClassVar, Literal

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates

from ...bases import Data
from ...custom_types import samplesheet_str, xenium_slide_serial_number
from ..data import DataSet, Sample


class XeniumRun(Data):
    __tablename__ = 'xenium_run'

    # XeniumRun attributes
    date_run_began: Mapped[date] = mapped_column(repr=False)

    # Model metadata
    id_date_col: ClassVar[Literal['date_run_began']] = 'date_run_began'
    id_prefix: ClassVar[Literal['XR']] = 'XR'
    id_length: ClassVar[Literal[7]] = 7

    # Child models
    data_sets: Mapped[list['XeniumDataSet']] = relationship(
        back_populates='xenium_run', default_factory=list, repr=False, compare=False
    )


class XeniumDataSet(DataSet, kw_only=True):
    # XeniumDataSet attributes
    slide_serial_number: Mapped[xenium_slide_serial_number | None]
    slide_name: Mapped[samplesheet_str | None]

    # Parent foreign keys
    xenium_run_id: Mapped[int | None] = mapped_column(
        ForeignKey('xenium_run.id'), init=False, repr=False
    )

    # Parent models
    xenium_run: Mapped[XeniumRun] = relationship(back_populates='data_sets')

    # Child models
    samples: Mapped[list['XeniumSample']] = relationship(
        back_populates='data_set', default_factory=list, repr=False
    )

    # Model metadata
    id_prefix: ClassVar[Literal['XD']] = 'XD'
    id_length: ClassVar[Literal[9]] = 9

    __mapper_args__ = {'polymorphic_identity': 'Xenium'}

    # TODO: implement this to check against 10x's database?
    # TODO: validate that it's actually an integer with the proper length
    @validates('slide_serial_number')
    def check_slide_serial_number(self, key: str, serial_number: str) -> str:
        return serial_number.strip()


class XeniumSample(Sample):
    # Parent models
    data_set: Mapped[XeniumDataSet] = relationship(back_populates='samples')

    # Model metadata
    id_prefix: ClassVar[Literal['XE']] = 'XE'
    id_length: ClassVar[Literal[9]] = 9

    __mapper_args__ = {'polymorphic_identity': 'Xenium'}
