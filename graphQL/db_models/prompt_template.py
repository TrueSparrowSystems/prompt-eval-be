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
    
    #Write method to get prompt by prompt id
    @classmethod
    def prompt_by_id(cls, prompt_id):
        return cls.objects.get(id=prompt_id)