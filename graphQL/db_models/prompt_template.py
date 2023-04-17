from enum import Enum
import time
from mongoengine import Document
from mongoengine.fields import (
    StringField,
    ObjectIdField,
    ListField,
    IntField,
   
)

    
class PromptTemplate(Document):
    meta = {'collection': 'prompt_template'}
    name = StringField(required=True)
    description = StringField(max_length=255)
    conversation = ListField()
    experiment_id = ObjectIdField(required=True)
    created_at = IntField(default=lambda: int(time.time()))
    updated_at = IntField(default=lambda: int(time.time()))