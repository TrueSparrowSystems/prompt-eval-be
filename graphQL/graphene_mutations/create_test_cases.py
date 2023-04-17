import graphene
from graphQL.graphene_types.test_case import TestCaseType, InputDynamicVarType
from graphQL.db_models.test_case import TestCase
from .mutation_base import MutateBase

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

        testCase = TestCase(name=name, experiment_id=experimentId)
        if 'description' in kwargs:
            testCase.description = kwargs['description']
        if 'dynamic_var_values' in kwargs:
            testCase.dynamic_var_values = kwargs['dynamic_var_values']
        if 'expected_result' in kwargs:
            testCase.expected_result = kwargs['expected_result']
        
        testCase.save()
        return CreateTestCasesMutation(testCase=testCase)