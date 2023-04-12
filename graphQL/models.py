from mongoengine import Document
from mongoengine.fields import (
    StringField,
    ObjectIdField
)

class Experiment(Document):
    meta = {'collection': 'experiment'}
    _id = ObjectIdField()
    name = StringField(required=True)
    description = StringField(max_length=50, required=True)

class Example(Document):
    meta = {'collection': 'example'}
    _id = ObjectIdField()
    name = StringField(required=True)
    description = StringField(max_length=50, required=True)
