from pytest import mark, raises

from scbl_db.models.platforms.xenium import *
from scbl_db.models.processes import *


class TestXeniumRun:
    """
    Tests for the XeniumRun model.
    """

    pass


class TestXeniumDataSet:
    """
    Tests for the XeniumDataSet model.
    """

    def test_platform_assignment(self, xenium_data_set: XeniumDataSet):
        assert xenium_data_set.platform_name == 'Xenium'

    def test_non_int_slide_serial_number(self, xenium_data_set: XeniumDataSet):
        with raises(ValueError):
            XeniumDataSet(
                id=xenium_data_set.id,
                slide_serial_number='string',
                slide_name=xenium_data_set.slide_name,
                xenium_run=xenium_data_set.xenium_run,
                date_initialized=xenium_data_set.date_initialized,
                lab=xenium_data_set.lab,
                submitter=xenium_data_set.submitter,
                assay=xenium_data_set.assay,
                ilab_request_id=xenium_data_set.ilab_request_id,
            )

    @mark.parametrize(argnames='slide_serial_number', argvalues=['000000', '00000000'])
    def test_wrong_length_slide_serial_number(
        self, slide_serial_number: str, xenium_data_set: XeniumDataSet
    ):
        with raises(ValueError):
            XeniumDataSet(
                id=xenium_data_set.id,
                slide_serial_number=slide_serial_number,
                slide_name=xenium_data_set.slide_name,
                xenium_run=xenium_data_set.xenium_run,
                date_initialized=xenium_data_set.date_initialized,
                lab=xenium_data_set.lab,
                submitter=xenium_data_set.submitter,
                assay=xenium_data_set.assay,
                ilab_request_id=xenium_data_set.ilab_request_id,
            )


class TestXeniumSample:
    """
    Tests for the XeniumSample model.
    """

    def test_platform_assignment(self, xenium_region: XeniumRegion):
        assert xenium_region.platform_name == 'Xenium'
