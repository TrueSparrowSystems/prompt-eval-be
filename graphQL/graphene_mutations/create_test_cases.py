import graphene
from graphQL.graphene_types.test_case import TestCaseType
from graphQL.db_models.test_case import TestCase
from .mutation_base import MutateBase
from graphQL.lib.helper import CommonValiator
from graphQL.lib.custom_exception import InvalidLengthError

class TestCaseInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    description = graphene.String()
    dynamic_var_values = graphene.JSONString()
    experiment_id = graphene.ID(required=True)
    expected_result = graphene.List(graphene.String)
class CreateTestCasesMutation(MutateBase):
    class Arguments:
        test_case_data = TestCaseInput(required=True)

    testCase = graphene.Field(TestCaseType)

    @classmethod
    def self_mutate(cls, root, info, test_case_data=None):
        if not CommonValiator.max_length_validation(test_case_data.name, 70):
            raise InvalidLengthError(code = "g_gm_ctc_1", param="name")       

        testCase = TestCase(name=test_case_data.name, experiment_id=test_case_data.experiment_id)
        if test_case_data.description:
            if not CommonValiator.max_length_validation(test_case_data.description, 240):
                raise InvalidLengthError(code = "g_gm_ctc_2", param="description") 
            testCase.description = test_case_data.description
        if test_case_data.dynamic_var_values:
            testCase.dynamic_var_values = test_case_data.dynamic_var_values
        if test_case_data.expected_result:
            testCase.expected_result = test_case_data.expected_result
        testCase.status = 'ACTIVE'
        testCase.save()
        return CreateTestCasesMutation(testCase=testCase)