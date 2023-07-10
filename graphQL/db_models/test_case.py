from graphQL.db_models.model_base import ModelBase
from mongoengine.fields import (
    StringField,
    ObjectIdField,
    ListField,
    DictField,

    EnumField
)
from enum import Enum

class Status(Enum):
    ACTIVE = 'ACTIVE'
    DELETED = 'DELETED'
    DISABLED = 'DISABLED'

    def __str__(self):
        return self.value

class TestCase(ModelBase):
    meta = {'collection': 'test_cases'}
    name = StringField(required=True)
    description = StringField(max_length=255)
    dynamic_var_values = DictField()
    experiment_id = ObjectIdField(required=True)
    expected_result= ListField()
    status = EnumField(Status)

    @classmethod
    def test_case_by_id(cls, prompt_id):
        return cls.objects.get(id=prompt_id)