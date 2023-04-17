from mongoengine import Document
from mongoengine.fields import (
    StringField,
    ObjectIdField,
    ListField,
    DictField,
    IntField,
)
import time

class TestCase(Document):
    meta = {'collection': 'test_cases'}
    name = StringField(required=True)
    description = StringField(max_length=255)
    dynamic_var_values = ListField()
    experiment_id = ObjectIdField(required=True)
    expected_result= ListField()
    created_at = IntField(default=lambda: int(time.time()))
    updated_at = IntField(default=lambda: int(time.time()))