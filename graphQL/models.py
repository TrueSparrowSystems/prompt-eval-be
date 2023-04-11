from mongoengine import Document
from mongoengine.fields import (
    StringField,
    ObjectIdField
)

class Experiment(Document):
    meta = {'collection': 'experiment'}
    ID = ObjectIdField()
    name = StringField(required=True)
    description = StringField(required=True)
