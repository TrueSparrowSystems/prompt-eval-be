from graphQL.db_models.model_base import ModelBase
from mongoengine.fields import (
    StringField,
    ObjectIdField,
    ListField,
    FloatField,
    IntField
)

class EvaluationTestCaseRelation(ModelBase):
    meta = {'collection': 'evaluation_test_case_relation'}
    evaluation_id = ObjectIdField(required=True)
    prompt = ListField(required=True)
    test_case_id = ObjectIdField(required=True)
    test_case_name = StringField()
    test_case_description = StringField()
    actual_result = ListField()
    acceptable_result = ListField()
    accuracy = FloatField()
    jsonl_order = IntField()
