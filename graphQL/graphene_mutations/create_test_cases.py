import graphene
from graphQL.graphene_types.test_case import TestCaseType
from graphQL.db_models.test_case import TestCase, Status as TestCaseStatus
from .mutation_base import MutateBase
from graphQL.lib.helper import CommonValidator
from graphQL.lib.custom_exception import InvalidLengthError, InvalidStatusError

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

    """
    create test case

    @params {Object} test_case_data
    @params {String} test_case_data.name
    @params {String} test_case_data.description
    @params {String} test_case_data.dynamic_var_values
    @params {String} test_case_data.experiment_id
    @params {String} test_case_data.expected_result

    @returns {Object} CreateTestCasesMutation object
    """
    @classmethod
    def self_mutate(cls, root, info, test_case_data=None):
        if not CommonValidator.max_length_validation(test_case_data.name, 70):
            raise InvalidLengthError(code = "g_gm_ctc_1", param="name")

        testCase = TestCase(name=test_case_data.name, experiment_id=test_case_data.experiment_id)
        if test_case_data.description:
            if not CommonValidator.max_length_validation(test_case_data.description, 240):
                raise InvalidLengthError(code = "g_gm_ctc_2", param="description")
            testCase.description = test_case_data.description
        if test_case_data.dynamic_var_values:
            testCase.dynamic_var_values = test_case_data.dynamic_var_values
        if test_case_data.expected_result:
            testCase.expected_result = test_case_data.expected_result
        if not (test_case_data.status == TestCaseStatus.ACTIVE.value or test_case_data.status == TestCaseStatus.DISABLED.value):
            raise InvalidStatusError(code = "g_gm_ctc_3", param="status") 
        testCase.status = test_case_data.status
        
        testCase.save()
        return CreateTestCasesMutation(testCase=testCase)