import graphene
from graphQL.graphene_types.test_case import TestCaseType
from graphQL.db_models.test_case import TestCase, Status as TestCaseStatus
from .mutation_base import MutateBase
from graphQL.lib.helper import CommonValidator
from graphQL.lib.custom_exception import InvalidLengthError, InvalidStatusError, ObjectNotFoundError
import logging

class UpdateTestCaseInput(graphene.InputObjectType):
    id = graphene.String(required=True)
    name = graphene.String()
    status = graphene.String()
    description = graphene.String()
    dynamic_var_values = graphene.JSONString()
    expected_result = graphene.List(graphene.String)

class UpdateTestCasesMutation(MutateBase):
    class Arguments:
        update_test_case_data = UpdateTestCaseInput(required=True)

    testCase = graphene.Field(TestCaseType)

    """
    update test case

    @params {Object} update_test_case_data
    @params {String} update_test_case_data.id
    @params {String} update_test_case_data.name
    @params {String} update_test_case_data.description
    @params {String} update_test_case_data.dynamic_var_values
    @params {String} update_test_case_data.expected_result
    @params {String} update_test_case_data.status

    @returns {Object} UpdateTestCasesMutation object
    """
    @classmethod
    def self_mutate(cls, root, info, update_test_case_data=None):
        testCase = ""
        try:
            testCase = TestCase.objects.get(id=update_test_case_data.id, status__in=[TestCaseStatus.ACTIVE.value, TestCaseStatus.DISABLED.value])
        except TestCase.DoesNotExist as e:
            logging.error("ERROR: ", e)
            raise ObjectNotFoundError(code="g_gm_utc_0", param="id", message="Testcase object not found")

        if update_test_case_data.name:
            if not CommonValidator.max_length_validation(update_test_case_data.name, 70):
                raise InvalidLengthError(code = "g_gm_utc_1", param="name")
            testCase.name = update_test_case_data.name

        if update_test_case_data.description:
            if not CommonValidator.max_length_validation(update_test_case_data.description, 240):
                raise InvalidLengthError(code = "g_gm_utc_2", param="description")
            testCase.description = update_test_case_data.description

        if update_test_case_data.dynamic_var_values:
            testCase.dynamic_var_values = update_test_case_data.dynamic_var_values

        if update_test_case_data.expected_result:
            testCase.expected_result = update_test_case_data.expected_result

        if update_test_case_data.status:
            if not (testCase.status == TestCaseStatus.ACTIVE.value or testCase.status == TestCaseStatus.DISABLED.value):
                raise InvalidStatusError(code = "g_gm_utc_3", param="status")
            testCase.status = update_test_case_data.status

        testCase.save()
        return UpdateTestCasesMutation(testCase=testCase)