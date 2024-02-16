from datetime import date

from scbl_db.models.data import DataSet, Platform
from scbl_db.models.entities import Lab

from .fixtures import delivery_parent_dir, institution, lab, person, platform


class TestDataSet:
    """
    Tests for the `data_set` model.
    """

    def test_same_batch_id(self, lab: Lab, platform: Platform):
        """
        Test that two `DataSet`s with the same date submitted and the
        same sample submitter have the same batch ID.
        """
        data_set_ids = (
            platform.data_set_id_prefix + f'{i:0{platform.data_set_id_length}}'
            for i in range(2)
        )
        data_sets = [
            DataSet(
                id=id,
                date_initialized=date.today(),
                lab=lab,
                platform=platform,
                submitter=lab.pi,
                ilab_request_id='ilab_request_id',
                name='data_set',
            )
            for id in data_set_ids
        ]

        assert data_sets[0].batch_id == data_sets[1].batch_id
