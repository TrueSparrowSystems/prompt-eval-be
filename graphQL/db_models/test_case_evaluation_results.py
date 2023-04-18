from graphQL.db_models.model_base import ModelBase
from mongoengine.fields import (
    StringField,
    ObjectIdField,
    ListField,
    FloatField
)

class TestCaseEvaluationResults(ModelBase):
    meta = {'collection': 'test_case_evaluation_results'}
    evaluation_result_id = ObjectIdField(required=True)
    prompt = StringField(required=True)
    test_case_id = ObjectIdField(required=True)
    test_case_name = StringField()
    test_case_description = StringField()
    actual_result = ListField()
    acceptable_result = ListField()
    accuracy = FloatField()