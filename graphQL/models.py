from enum import Enum
from mongoengine import Document
from mongoengine.fields import (
    StringField,
    ObjectIdField,
    ListField,
    DictField,
    FloatField,
    IntField,
    EnumField,
    DateTimeField
)

class Experiment(Document):
    meta = {'collection': 'experiment'}
    _id = ObjectIdField()
    name = StringField(required=True)
    description = StringField(max_length=255)
    dyanamic_vars = ListField()
    created_at = IntField()
    updated_at = IntField()

class Example(Document):
    meta = {'collection': 'example'}
    _id = ObjectIdField()
    name = StringField(required=True)
    description = StringField(max_length=50, required=True)
    
class PromptTemplate(Document):
    meta = {'collection': 'prompt_template'}
    _id = ObjectIdField()
    name = StringField(required=True)
    description = StringField(max_length=255)
    conversation = ListField()
    experiment_id = ObjectIdField()
    created_at = IntField()
    updated_at = IntField()

class Testcase(Document):
    meta = {'collection': 'test_cases'}
    _id = ObjectIdField()
    name = StringField(required=True)
    description = StringField(max_length=255)
    dynamic_var_values = DictField()
    experiment_id = ObjectIdField(required=True)
    expected_result= ListField()
    created_at = IntField()
    updated_at = IntField()


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

