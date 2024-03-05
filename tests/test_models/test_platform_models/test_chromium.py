from datetime import date

from pytest import mark, raises

from scbl_db.models.platforms.chromium import *
from scbl_db.models.processes import *


class TestcChromiumDataSet:
    """
    Tests for the ChromiumDataSet model.
    """

    def test_platform_assignment(self, chromium_data_set: ChromiumDataSet):
        assert chromium_data_set.platform_name == 'Chromium'


class TestChromiumSample:
    """
    Tests for the ChromiumSample model.
    """

    def test_platform_assignment(self, chromium_sample: ChromiumSample):
        assert chromium_sample.platform_name == 'Chromium'


class TestSequencingRun:
    """
    Tests for the SequencingRun model.
    """

    id = '99-scbct-000'
    date_begun = date(1999, 1, 1)

    def test_wrong_year_id(self, sequencing_run: SequencingRun):
        correct_year = sequencing_run.id[:2]
        wrong_year = str(int(correct_year) + 1)
        wrong_year_id = sequencing_run.id.replace(correct_year, wrong_year)

        with raises(ValueError):
            SequencingRun(id=wrong_year_id, date_begun=sequencing_run.date_begun)

    @mark.parametrize(argnames='id', argvalues=['99-scbct-0', '99-scbct-0000'])
    def test_wrong_length_id(self, id: str, sequencing_run: SequencingRun):
        with raises(ValueError):
            SequencingRun(id=id, date_begun=sequencing_run.date_begun)
