from sqlalchemy import create_engine, inspect, select
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    MappedAsDataclass,
    mapped_column,
    sessionmaker,
)

from scbl_db import Base, ChromiumDataSet, Institution, Lab, Person

engine = create_engine('sqlite:///db.sqlite')
Base.metadata.create_all(engine)

session_maker = sessionmaker(engine)

with session_maker.begin() as session:

    new_inst = Institution(
        ror_id='02der9h97', email_format=r'{first_name}.{last_name}@uconn.edu'
    )
    other_inst = session.merge(new_inst)
    session.add(other_inst)
    print(session.execute(select(Institution)).scalars().all())
