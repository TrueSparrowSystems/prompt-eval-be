from graphQL.db_models.model_base import ModelBase
from mongoengine.fields import (
    StringField,
    ObjectIdField,
    ListField,
    DictField,
    IntField,
)

class TestCase(ModelBase):
    meta = {'collection': 'test_cases'}
    name = StringField(required=True)
    description = StringField(max_length=255)
    dynamic_var_values = DictField()
    experiment_id = ObjectIdField(required=True)
    expected_result= ListField()