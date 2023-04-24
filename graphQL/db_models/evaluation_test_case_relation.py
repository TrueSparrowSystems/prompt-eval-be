from graphQL.db_models.model_base import ModelBase
from mongoengine.fields import (
    StringField,
    ObjectIdField,
    ListField,
    FloatField
)

class EvaluationTestCaseRelation(ModelBase):
    meta = {'collection': 'test_case_evaluation_results'}
    evaluation_result_id = ObjectIdField(required=True)
    prompt = StringField(required=True)
    test_case_id = ObjectIdField(required=True)
    test_case_name = StringField()
    test_case_description = StringField()
    actual_result = ListField()
    acceptable_result = ListField()
    accuracy = FloatField()

    @classmethod
    def create_evaluation_test_case_relation(cls, params):
        try:
            
            evaluation_test_case_relation = cls()
            evaluation_test_case_relation.evaluation_result_id = params['evaluation_result_id']
            evaluation_test_case_relation.prompt = params['prompt']
            evaluation_test_case_relation.test_case_id = params['test_case_id']
            evaluation_test_case_relation.test_case_name = params['test_case_name'] 
            evaluation_test_case_relation.test_case_description = params['test_case_description'] 
            evaluation_test_case_relation.acceptable_result = params['acceptable_result']
            
            if params.get('accuracy') and params.get('actual_result'):
                evaluation_test_case_relation.accuracy = params['accuracy'] 
                evaluation_test_case_relation.actual_result = params['actual_result']
                
            evaluation_test_case_relation.save()
        
        except Exception as e:
            print("Error in create_evaluation_test_case_relation method", e)
            return False
        
        return evaluation_test_case_relation
        
    @classmethod
    def bulk_create_evaluation_test_case_relation(cls, params):
        evaluation_test_case_relations = []
        for param in params:
            evaluation_test_case_relation = cls()
            evaluation_test_case_relation.evaluation_result_id = param['evaluation_result_id']
            #evaluation_test_case_relation.prompt = param['prompt']
            evaluation_test_case_relation.test_case_id = param['test_case_id']
            evaluation_test_case_relation.test_case_name = param['test_case_name'] 
            evaluation_test_case_relation.test_case_description = param['test_case_description'] 
            evaluation_test_case_relation.acceptable_result = param['acceptable_result']
            
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
 