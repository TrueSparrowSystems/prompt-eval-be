import json
from graphene_django.utils.testing import GraphQLTestCase
from graphQL.db_models.experiment import Experiment
from graphQL.db_models.test_case import TestCase

# Command to run test cases for experiment
# $ python manage.py test graphQL.test.test_testcase
# Create your tests here.
class TestcasesTest(GraphQLTestCase):

    def test_get_testcases_query(self):
        experiment = Experiment.objects.create(name="Test Experiment", description="This is a test experiment")
        variable = {'experimentId': str(experiment.id)}
        response = self.query(
            '''
            query testCases($experimentId: String!) {
                    testCases(experimentId: $experimentId ) {
                        id
                        name
                        description
                        dynamicVarValues
                        experimentId
                        expectedResult
                        updatedAt
                        createdAt
                    }
                }
            ''', variables=variable
          )

        content = json.loads(response.content)

        # This validates the status code and if you get errors
        self.assertResponseNoErrors(response)
        Experiment.objects.filter(id=experiment.id).delete()
        # Add some more asserts if you like
      
    def test_create_active_testcase_mutation(self):
        experiment = Experiment.objects.create(name="Test Experiment", description="This is a test experiment")
        variable = {"experimentId": str(experiment.id), "dynamicVarValues": json.dumps({"key":"hey","value":"value"})}
        response = self.query(
            '''
            mutation createTestCase($experimentId: ID!, $dynamicVarValues: JSONString) {
                createTestCases(testCaseData:{
                    experimentId:$experimentId,
                    name:"new Testcase",
                    status:"ACTIVE",
                    dynamicVarValues:$dynamicVarValues,
                    expectedResult:["hey","hey10"]}
                ) {
                    testCase {
                    id
                    name
                    status
                    description
                    expectedResult
                    dynamicVarValues
                    createdAt
                    updatedAt
                    experimentId
                    }
                }
            }
            ''', variables=variable
        )

        content = json.loads(response.content)
        # This validates the status code and if you get errors
        self.assertResponseNoErrors(response)
        self.assertEqual(content['data']['createTestCases']['testCase']['name'], 'new Testcase')

        Experiment.objects.filter(id=experiment.id).delete()
        TestCase.objects.filter(id=content['data']['createTestCases']['testCase']['id']).delete()

    def test_create_disabled_testcase_mutation(self):
        experiment = Experiment.objects.create(name="Test Experiment", description="This is a test experiment")
        variable = {"experimentId": str(experiment.id), "dynamicVarValues": json.dumps({"key":"hey","value":"value"})}
        response = self.query(
            '''
            mutation createTestCase($experimentId: ID!, $dynamicVarValues: JSONString) {
                createTestCases(testCaseData:{
                    experimentId:$experimentId,
                    name:"new Testcase",
                    status:"DISABLED",
                    dynamicVarValues:$dynamicVarValues,
                    expectedResult:["hey","hey10"]}
                ) {
                    testCase {
                    id
                    name
                    status
                    description
                    expectedResult
                    dynamicVarValues
                    createdAt
                    updatedAt
                    experimentId
                    }
                }
            }
            ''', variables=variable
        )

        content = json.loads(response.content)
        # This validates the status code and if you get errors
        self.assertResponseNoErrors(response)
        self.assertEqual(content['data']['createTestCases']['testCase']['name'], 'new Testcase')

        Experiment.objects.filter(id=experiment.id).delete()
        TestCase.objects.filter(id=content['data']['createTestCases']['testCase']['id']).delete()


    def test_create_deleted_testcase_mutation(self):
        experiment = Experiment.objects.create(name="Test Experiment", description="This is a test experiment")
        variable = {"experimentId": str(experiment.id), "dynamicVarValues": json.dumps({"key":"hey","value":"value"})}
        response = self.query(
            '''
            mutation createTestCase($experimentId: ID!, $dynamicVarValues: JSONString) {
                createTestCases(testCaseData:{
                    experimentId:$experimentId,
                    name:"new Testcase",
                    status:"DELETED",
                    dynamicVarValues:$dynamicVarValues,
                    expectedResult:["hey","hey10"]}
                ) {
                    testCase {
                    id
                    name
                    status
                    description
                    expectedResult
                    dynamicVarValues
                    createdAt
                    updatedAt
                    experimentId
                    }
                }
            }
            ''', variables=variable
        )

        content = json.loads(response.content)
        # This validates the status code and if you get errors
        self.assertResponseHasErrors(response)
        self.assertEqual(content['errors'][0]['message'], "Invalid status")

        Experiment.objects.filter(id=experiment.id).delete()

    
    def test_create_testcase_mocked_mutations(self):
        experiment = Experiment.objects.create(name="Test Experiment", description="This is a test experiment")
        variable = {"experimentId": str(experiment.id), "dynamicVarValues": json.dumps({"key":"hey","value":"value"})}
        response = self.query(
            '''
            mutation createTestCase($experimentId: ID!, $dynamicVarValues: JSONString) {
                createTestCases(testCaseData:{
                    name:"new Testcase",
                    dynamicVarValues:$dynamicVarValues,
                    expectedResult:["hey","hey10"]}
                ) {
                    testCase {
                    id
                    name
                    description
                    expectedResult
                    dynamicVarValues
                    createdAt
                    updatedAt
                    experimentId
                    }
                }
            }
            ''', variables=variable
        )

        content = json.loads(response.content)
        # This validates the status code and if you get errors
        self.assertResponseHasErrors(response)
        self.assertEqual(content['errors'][0]['message'], "Field 'TestCaseInput.experimentId' of required type 'ID!' was not provided.")
        Experiment.objects.filter(id=experiment.id).delete()

    
    def test_update_testcase_to_disabled_mutation(self):
        experiment = Experiment.objects.create(name="Test Experiment", description="This is a test experiment")
        testcase = TestCase.objects.create(name="Testcase", description="This is a test testcase", experiment_id=str(experiment.id), status = "ACTIVE")
        variable = {"id": str(testcase.id), "dynamicVarValues": json.dumps({"key":"hey","value":"value"}), "status": "DISABLED"}
        response = self.query(
            '''
            mutation updateTestCase($id: String!, $dynamicVarValues: JSONString, $status: String) {
                updateTestCases(updateTestCaseData:{
                    id:$id,
                    name:"new Testcase",
                    status:$status,
                    dynamicVarValues:$dynamicVarValues,
                    expectedResult:["hey","hey10"]}
                ) {
                    testCase {
                    id
                    name
                    description
                    expectedResult
                    dynamicVarValues
                    createdAt
                    updatedAt
                    experimentId
                    }
                }
            }
            ''', variables=variable
        )

        content = json.loads(response.content)
        # This validates the status code and if you get errors
        self.assertResponseNoErrors(response)
        self.assertEqual(content['data']['updateTestCases']['testCase']['name'], 'new Testcase')

        Experiment.objects.filter(id=experiment.id).delete()
        TestCase.objects.filter(id=testcase.id).delete()

    
    def test_update_testcase_to_deleted_mutation(self):
        experiment = Experiment.objects.create(name="Test Experiment", description="This is a test experiment")
        testcase = TestCase.objects.create(name="Testcase", description="This is a test testcase", experiment_id=str(experiment.id), status = "ACTIVE")
        variable = {"id": str(testcase.id), "dynamicVarValues": json.dumps({"key":"hey","value":"value"}), "status": "DELETED"}
        response = self.query(
            '''
            mutation updateTestCase($id: String!, $dynamicVarValues: JSONString, $status: String) {
                updateTestCases(updateTestCaseData:{
                    id:$id,
                    name:"new Testcase",
                    status:$status,
                    dynamicVarValues:$dynamicVarValues,
                    expectedResult:["hey","hey10"]}
                ) {
                    testCase {
                    id
                    name
                    description
                    expectedResult
                    dynamicVarValues
                    createdAt
                    updatedAt
                    experimentId
                    }
                }
            }
            ''', variables=variable
        )

        content = json.loads(response.content)
        # This validates the status code and if you get errors
        self.assertResponseHasErrors(response)
        self.assertEqual(content['errors'][0]['message'], "Invalid status")

        Experiment.objects.filter(id=experiment.id).delete()
        TestCase.objects.filter(id=testcase.id).delete()


    def test_update_testcase_mocked_mutations(self):
        experiment = Experiment.objects.create(name="Test Experiment", description="This is a test experiment")
        testcase = TestCase.objects.create(name="Testcase", description="This is a test testcase", experiment_id=str(experiment.id))
        variable = {"id": str(testcase.id), "dynamicVarValues": json.dumps({"key":"hey","value":"value"})}
        response = self.query(
            '''
            mutation updateTestCase($id: String!, $dynamicVarValues: JSONString) {
                updateTestCases(updateTestCaseData:{
                    name:"new Testcase",
                    dynamicVarValues:$dynamicVarValues,
                    expectedResult:["hey","hey10"]}
                ) {
                    testCase {
                    id
                    name
                    description
                    expectedResult
                    dynamicVarValues
                    createdAt
                    updatedAt
                    experimentId
                    }
                }
            }
            ''', variables=variable
        )

        content = json.loads(response.content)
        # This validates the status code and if you get errors
        self.assertResponseHasErrors(response)
        self.assertEqual(content['errors'][0]['message'], "Field 'UpdateTestCaseInput.id' of required type 'String!' was not provided.")

        Experiment.objects.filter(id=experiment.id).delete()
        TestCase.objects.filter(id=testcase.id).delete()
