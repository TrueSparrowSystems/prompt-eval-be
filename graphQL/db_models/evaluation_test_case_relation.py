from graphQL.db_models.model_base import ModelBase
from mongoengine.fields import (
    StringField,
    ObjectIdField,
    ListField,
    FloatField,
    IntField
)

class EvaluationTestCaseRelation(ModelBase):
    meta = {'collection': 'evaluation_test_case_relations'}
    evaluation_id = ObjectIdField(required=True)
    prompt = ListField(required=True)
    test_case_id = ObjectIdField(required=True)
    test_case_name = StringField()
    test_case_description = StringField()
    actual_result = ListField()
    acceptable_result = ListField()
    accuracy = FloatField(null=True)
    jsonl_order = IntField()

    """
    Bulk creates evaluation test case relations.
    
    @params {Object} params
    @params {String} params.evaluation_id
    @params {String} params.prompt
    @params {String} params.test_case_id
    @params {String} params.test_case_name
    @params {String} params.test_case_description
    @params {String} params.acceptable_result
    @params {String} params.jsonl_order
    @params {String} params.accuracy
    @params {String} params.actual_result   

    @returns {Object} evaluation_test_case_relations
    """
    @classmethod
    def bulk_create_evaluation_test_case_relation(cls, params):
        evaluation_test_case_relations = []
        for param in params:
            evaluation_test_case_relation = cls()
            evaluation_test_case_relation.evaluation_id = param['evaluation_id']
            evaluation_test_case_relation.prompt = param['prompt']
            evaluation_test_case_relation.test_case_id = param['test_case_id']
            evaluation_test_case_relation.test_case_name = param['test_case_name'] 
            evaluation_test_case_relation.test_case_description = param['test_case_description'] 
            evaluation_test_case_relation.acceptable_result = param['acceptable_result']
            evaluation_test_case_relation.jsonl_order = param['jsonl_order']
            
            if param.get('accuracy') and param.get('actual_result'):
                evaluation_test_case_relation.accuracy = param['accuracy'] 
                evaluation_test_case_relation.actual_result = param['actual_result']
                
            evaluation_test_case_relations.append(evaluation_test_case_relation)
        print("evaluation_test_case_relations length:   ", len(evaluation_test_case_relations))
            
        try:
            cls.objects.insert(evaluation_test_case_relations)
        except Exception as e:
            print("Error in bulk_create_evaluation_test_case_relation method", e)
            return False
        
        return evaluation_test_case_relations
    
    """
    Updates evaluation test case relation.

    @params {Object} params
    @params {String} params.evaluation_id
    @params {String} params.jsonl_order
    @params {String} params.actual_result
    @params {String} params.accuracy

    @returns {Boolean} 
    """
    @classmethod
    def update_evaluation_test_case_relation(cls, params):
        try:
            cls.objects(evaluation_id=params['evaluation_id'], jsonl_order=params['jsonl_order']).update(
                set__actual_result=params['actual_result'], set__accuracy=params['accuracy'])
        except Exception as e:
            print("Error in update_evaluation_test_case_relation method", e)
            return False
        
        return True
    
    """
    Deletes evaluation test case relation records by evaluation ID.

    @params {String} evaluation_id

    @returns {Boolean}
    """
    @classmethod
    def delete_records_by_evaluation_id(cls, evaluation_id):

        try:
            cls.objects(evaluation_id=evaluation_id).delete()
        except Exception as e:
            print("Error in delete_records method", e)
            return False
        
        return True
