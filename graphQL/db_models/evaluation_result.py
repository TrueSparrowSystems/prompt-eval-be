from enum import Enum
from mongoengine import Document
from mongoengine.fields import (
    StringField,
    ObjectIdField,
    DictField,
    FloatField,
    IntField,
    EnumField,
    DateTimeField
)

class Status(Enum):
    INITIATED = 'INITIATED'
    COMPLETED = 'COMPLETED'
    RUNNING = 'RUNNING'
    FAILED = 'FAILED'

class EvaluationResult(Document):
    meta = {'collection': 'evaluation_results'}
    _id = ObjectIdField()
    model = StringField(required=True)
    eval = StringField(required=True)
    accuracy = FloatField()
    prompt_template_id = ObjectIdField(required=True)
    evaluation_report_data = DictField()
    run_id = IntField()
    status = EnumField(Status, default=Status.INITIATED)
    completed_at = DateTimeField()
    created_at = IntField()
    updated_at = IntField()