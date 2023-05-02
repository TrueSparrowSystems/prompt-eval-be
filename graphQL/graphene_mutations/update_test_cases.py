import graphene
from graphQL.db_models.test_case import TestCase
from graphQL.graphene_types.test_case import TestCaseType
from .mutation_base import MutateBase
from graphQL.lib.helper import CommonValiator
from graphQL.lib.custom_exception import InvalidLengthError

class UpdateTestCaseInput(graphene.InputObjectType):
    id = graphene.String(required=True)
    name = graphene.String()
    description = graphene.String()
    dynamic_var_values = graphene.JSONString()
    expected_result = graphene.List(graphene.String)

class UpdateTestCasesMutation(MutateBase):
    class Arguments:
        update_test_case_data = UpdateTestCaseInput(required=True)

    testCase = graphene.Field(TestCaseType)

    @classmethod
    def self_mutate(cls, root, info, update_test_case_data=None):
        testCase = TestCase.objects.get(id=update_test_case_data.id)

        if update_test_case_data.name:
            if not CommonValiator.max_length_validation(update_test_case_data.name, 70):
                raise InvalidLengthError(code = "g_gm_utc_1", param="name")       
            testCase.name = update_test_case_data.name

        if update_test_case_data.description:
            if not CommonValiator.max_length_validation(update_test_case_data.description, 240):
                raise InvalidLengthError(code = "g_gm_utc_2", param="description") 
            testCase.description = update_test_case_data.description

        if update_test_case_data.dynamic_var_values:
            testCase.dynamic_var_values = update_test_case_data.dynamic_var_values

        if update_test_case_data.expected_result:
            testCase.expected_result = update_test_case_data.expected_result
        
        testCase.save()
        return UpdateTestCasesMutation(testCase=testCase)