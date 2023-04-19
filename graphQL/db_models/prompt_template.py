from mongoengine.fields import (
    StringField,
    ObjectIdField,
    ListField,
    IntField
)
from graphQL.db_models.model_base import ModelBase

    
class PromptTemplate(ModelBase):
    meta = {'collection': 'prompt_template'}
    name = StringField(required=True)
    description = StringField(max_length=255)
    conversation = ListField()
    experiment_id = ObjectIdField(required=True)