from mongoengine.fields import (
    StringField,
    ObjectIdField,
    ListField,
    IntField,
    EnumField
)
from graphQL.db_models.model_base import ModelBase
from enum import Enum

class Status(Enum):
    ACTIVE = 'ACTIVE'
    DELETED = 'DELETED'

    
class PromptTemplate(ModelBase):
    meta = {'collection': 'prompt_template'}
    name = StringField(required=True)
    description = StringField(max_length=255)
    conversation = ListField()
    experiment_id = ObjectIdField(required=True)
    status = EnumField(Status, default=Status.ACTIVE)
    
    #Write method to get prompt by prompt id
    @classmethod
    def prompt_by_id(cls, prompt_id):
        return cls.objects.get(id=prompt_id)