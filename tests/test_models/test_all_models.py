from dataclasses import MISSING

from pytest import mark
from sqlalchemy import inspect
from sqlalchemy.orm import RelationshipDirection

from scbl_db import ORDERED_MODELS, Base


# TODO: this test is super ugly, improve it
@mark.parametrize(
    argnames='model', argvalues=[model for model in ORDERED_MODELS.values()]
)
def test_model_parent_dataclass_features(model: type[Base]):
    relationships = inspect(model).relationships

    for relationship_name, relationship in relationships.items():
        if relationship_name == 'platform':
            continue

        dataclass_relationhip_field = next(
            field for field in model.fields() if field.name == relationship_name
        )

        assert (
            dataclass_relationhip_field.default is not MISSING
            or dataclass_relationhip_field.default_factory is not MISSING
        )
        assert dataclass_relationhip_field.init

        if relationship.direction != RelationshipDirection.MANYTOONE:
            continue

        foreign_key_name = f'{relationship_name}_id'

        dataclass_foreign_key_field = None
        for field in model.fields():
            if field.name == foreign_key_name:
                dataclass_foreign_key_field = field

        if dataclass_foreign_key_field is not None:
            assert (
                dataclass_foreign_key_field.default is not MISSING
                or dataclass_foreign_key_field.default_factory is not MISSING
            )
            assert dataclass_foreign_key_field.init
        elif relationship_name in ('assay', 'library_type'):
            pass
        else:
            raise ValueError(f'Foreign key {foreign_key_name} not found.')
