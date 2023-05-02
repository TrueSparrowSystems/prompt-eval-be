from enum import Enum
from time import time
from mongoengine.fields import (
    StringField,
    ObjectIdField,
    DictField,
    FloatField,
    IntField,
    EnumField,
    DateTimeField
)
from time import time
from graphQL.db_models.model_base import ModelBase

class Status(Enum):
    INITIATED = 'INITIATED'
    COMPLETED = 'COMPLETED'
    RUNNING = 'RUNNING'
    FAILED = 'FAILED'

class Evaluation(ModelBase):
    meta = {'collection': 'evaluation'}
    model = StringField(required=True)
    eval = StringField(required=True)
    accuracy = FloatField()
    prompt_template_id = ObjectIdField(required=True)
    run_id = IntField(default=lambda: 1)
    status = EnumField(Status, default=Status.INITIATED)
    eval_parameter = DictField()
    retry_count = IntField(default=lambda: 0)
    error_object = StringField()
    initiated_at = IntField(default=lambda: int(time()))
    completed_at = IntField()
    
    # Method to get the evaluation object by id
    @classmethod
    def evaluation_by_id(cls, evaluation_id):
        return cls.objects.get(id=evaluation_id)
