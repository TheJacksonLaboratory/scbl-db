from pathlib import Path

from pytest import fixture
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from scbl_db.bases import Base

__all__ = ['tmp_db_session']


@fixture
def tmp_db_session(tmp_path: Path) -> sessionmaker[Session]:
    """
    Create a temporary SQLite database and return a sessionmaker
    for it.
    """
    db_path = tmp_path / 'test.db'
    engine = create_engine(f'sqlite:///{db_path}')
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine)
