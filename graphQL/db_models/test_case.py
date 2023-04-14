from mongoengine import Document
from mongoengine.fields import (
    StringField,
    ObjectIdField,
    ListField,
    DictField,
    IntField,
)

class Testcase(Document):
    meta = {'collection': 'test_cases'}
    _id = ObjectIdField()
    name = StringField(required=True)
    description = StringField(max_length=255)
    dynamic_var_values = DictField()
    experiment_id = ObjectIdField(required=True)
    expected_result= ListField()
    created_at = IntField()
    updated_at = IntField()