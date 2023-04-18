from mongoengine.fields import (
    StringField,
    ListField,
    IntField,
)
from graphQL.db_models.model_base import ModelBase

class Experiment(ModelBase):
    meta = {'collection': 'experiment'}
    name = StringField(required=True)
    description = StringField(max_length=255)
    dynamic_vars = ListField(StringField(max_length=255))