from datetime import date
from typing import ClassVar, Literal

from pytest import raises
from sqlalchemy.orm import Mapped, mapped_column

from scbl_db.bases import Data


class TestEntity:
    pass


class TestData:
    """
    Tests for the abstract base class Data.
    """

    class DataSubclass(Data, kw_only=True):
        __tablename__ = 'data_subclass'
        date_info: Mapped[date] = mapped_column(repr=False)

        id_date_col: ClassVar[Literal['date_info']] = 'date_info'
        id_prefix: ClassVar[Literal['DA']] = 'DA'
        id_length: ClassVar[Literal[7]] = 7

    date_info = date(1999, 1, 1)

    def test_valid_id(self):
        data_subclass = self.DataSubclass(id='DA99000', date_info=self.date_info)
        assert data_subclass.id == 'DA99000'

    def test_wrong_year_id(self):
        """
        Test that an incorrectly formatted ID raises a ValueError.
        """
        with raises(ValueError):
            self.DataSubclass(id='DA24000', date_info=self.date_info)

    def test_wrong_length_id(self):
        """
        Test that an incorrectly formatted ID raises a ValueError.
        """
        with raises(ValueError):
            self.DataSubclass(id='DA990000', date_info=self.date_info)

    def test_wrong_prefix_id(self):
        """
        Test that an incorrectly formatted ID raises a ValueError.
        """
        with raises(ValueError):
            self.DataSubclass(id='AB99000', date_info=self.date_info)


class TestSomethingToChange:
    pass
