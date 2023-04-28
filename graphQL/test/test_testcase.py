import json
from graphene_django.utils.testing import GraphQLTestCase

# Command to run test cases for experiment
# $ python manage.py test graphQL.test.test_testcase
# Create your tests here.
class TestcasesTest(GraphQLTestCase):
    testcaseID = ""
    experimentId = ""

    def test_create_experiment_mutation(self):
        response = self.query(
            '''
            mutation{
                createExperiment(experimentData:{name:"Test Experiment",description:"This is a test experiment"}){
                    experiment {
                    id
                    name
                    description
                    dynamicVars
                    createdAt
                    updatedAt
                    }
                }
            }
            '''
        )

        content = json.loads(response.content)
        print('################################################\n')
        # This validates the status code and if you get errors
        self.assertResponseNoErrors(response)
        TestcasesTest.experimentID = content['data']['createExperiment']['experiment']['id']

    def test_get_testcases_query(self):
        variable = {"experimentId": TestcasesTest.experimentID}
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

        # Add some more asserts if you like
      
    def test_create_testcase_mutation(self):
        variable = {"experimentId": TestcasesTest.experimentID, "dynamicVarValues": json.dumps({"key":"hey","value":"value"})}
        # dynamicVarValues = {"key":"hey","value":"value"}
        dynamicVarValues = json.dumps({"key":"hey","value":"value"})
        response = self.query(
            '''
            mutation createTestCase($experimentId: ID!, $dynamicVarValues: JSONString) {
                createTestCases(testCaseData:{
                    experimentId:$experimentId,
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
        print('################################################\n')
        TestcasesTest.testcaseID = content['data']['createTestCases']['testCase']['id']
        # This validates the status code and if you get errors
        self.assertResponseNoErrors(response)
        self.assertEqual(content['data']['createTestCases']['testCase']['name'], 'new Testcase')

    
    def test_create_testcase_mocked_mutations(self):
        variable = {"experimentId": TestcasesTest.experimentID, "dynamicVarValues": json.dumps({"key":"hey","value":"value"})}
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
    
    def test_update_testcase_mutation(self):
        variable = {"id": TestcasesTest.testcaseID, "dynamicVarValues": json.dumps({"key":"hey","value":"value"})}
        response = self.query(
            '''
            mutation updateTestCase($id: String!, $dynamicVarValues: JSONString) {
                updateTestCases(updateTestCaseData:{
                    id:$id,
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
        self.assertResponseNoErrors(response)
        self.assertEqual(content['data']['updateTestCases']['testCase']['name'], 'new Testcase')

    def test_update_testcase_mocked_mutations(self):
        variable = {"id": TestcasesTest.testcaseID, "dynamicVarValues": json.dumps({"key":"hey","value":"value"})}
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
