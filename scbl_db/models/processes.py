from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..bases import Process

__all__ = ['Platform', 'Assay']


class Platform(Process, kw_only=True):
    __tablename__ = 'platform'

    assays: Mapped[list['Assay']] = relationship(
        back_populates='platform', default_factory=list, repr=False
    )


class Assay(Process, kw_only=True):
    __tablename__ = 'assay'

    # Parent foreign keys
    platform_name: Mapped[str] = mapped_column(
        ForeignKey('platform.name'), default=None, init=False, repr=False
    )

    platform: Mapped[Platform] = relationship(back_populates='assays', repr=False)
