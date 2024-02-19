from pytest import mark

import scbl_db.models.data
from scbl_db.bases import Data


@mark.parametrize(argnames='model_name', argvalues=scbl_db.models.data.__all__)
def test_all_data_are_Data(model_name: str):
    """
    Test that all models in `scbl_db.models.data` are subclasses of
    `scbl_db.bases.Data`.
    """
    model = getattr(scbl_db.models.data, model_name)
    assert issubclass(model, Data)
