import time
from mongoengine import Document
from mongoengine.fields import (
    StringField,
    ListField,
    IntField,
)

class Experiment(Document):
    meta = {'collection': 'experiment'}
    name = StringField(required=True)
    description = StringField(max_length=255)
    dynamic_vars = ListField(StringField(max_length=255))
    created_at = IntField(default=lambda: int(time.time()))
    updated_at = IntField(default=lambda: int(time.time()))