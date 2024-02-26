from inspect import get_annotations

import scbl_db as scbl_db
import scbl_db.models.entities as entities
import scbl_db.models.platforms.chromium as chromium
import scbl_db.models.platforms.xenium as xenium
import scbl_db.models.processes as processes


class TestInit:
    exported_model_names = set(
        entities.__all__ + chromium.__all__ + xenium.__all__ + processes.__all__
    )
    all_model_names = {
        mapper.class_.__name__ for mapper in scbl_db.Base.registry.mappers
    } - {'DataSet', 'Sample'}

    def test_exported_models(self):
        assert self.exported_model_names == self.all_model_names

    def test_ordered_models_instance_has_all_keys(self):
        assert (
            scbl_db.ORDERED_MODELS.keys()
            == get_annotations(scbl_db.OrderedModelDict).keys()
        )

    def test_all_models_are_ordered(self):
        assert scbl_db.ORDERED_MODELS.keys() == self.all_model_names
