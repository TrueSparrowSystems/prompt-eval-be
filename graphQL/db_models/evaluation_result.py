from enum import Enum
from mongoengine.fields import (
    StringField,
    ObjectIdField,
    DictField,
    FloatField,
    IntField,
    EnumField,
    DateTimeField
)
from graphQL.db_models.model_base import ModelBase

class Status(Enum):
    INITIATED = 'INITIATED'
    COMPLETED = 'COMPLETED'
    RUNNING = 'RUNNING'
    FAILED = 'FAILED'

class EvaluationResult(ModelBase):
    meta = {'collection': 'evaluation_results'}
    model = StringField(required=True)
    eval = StringField(required=True)
    accuracy = FloatField()
    prompt_template_id = ObjectIdField(required=True)
    evaluation_report_data = DictField()
    run_id = IntField()
    status = EnumField(Status, default=Status.INITIATED)
    completed_at = DateTimeField()