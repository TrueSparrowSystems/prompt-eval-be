import graphene
from graphQL.graphene_types.test_case import TestCaseType, InputDynamicVarType
from graphQL.db_models.test_case import TestCase
from .mutation_base import MutateBase
from graphQL.lib.helper import CommonValiator

class CreateTestCasesMutation(MutateBase):
    class Arguments:
        name = graphene.String(required=True)
        description = graphene.String()
        dynamic_var_values = graphene.List(InputDynamicVarType)
        experimentId = graphene.ID(required=True)
        expected_result = graphene.List(graphene.String)

    testCase = graphene.Field(TestCaseType)

    @staticmethod
    def self_mutate(root, info, name, experimentId, **kwargs):
        if not CommonValiator.length_validation(name, 70):
            raise Exception('Invalid name length')        

        testCase = TestCase(name=name, experiment_id=experimentId)
        if 'description' in kwargs:
            if not CommonValiator.length_validation(kwargs['description'], 240):
                raise Exception('Invalid description length')
            testCase.description = kwargs['description']
        if 'dynamic_var_values' in kwargs:
            testCase.dynamic_var_values = kwargs['dynamic_var_values']
        if 'expected_result' in kwargs:
            testCase.expected_result = kwargs['expected_result']
        
        testCase.save()
        return CreateTestCasesMutation(testCase=testCase)