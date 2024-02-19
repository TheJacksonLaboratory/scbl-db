from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..bases import SomethingToChange

__all__ = ['Platform', 'Assay']


class Platform(SomethingToChange, kw_only=True):
    __tablename__ = 'platform'


class Assay(SomethingToChange, kw_only=True):
    __tablename__ = 'assay'
    # Parent foreign keys
    platform_name: Mapped[str] = mapped_column(
        ForeignKey('platform.name'), init=False, repr=False
    )

    # Parent models
    platform: Mapped[Platform] = relationship()
