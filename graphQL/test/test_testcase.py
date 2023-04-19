import json
from graphene_django.utils.testing import GraphQLTestCase

# Command to run test cases for experiment
# $ python manage.py test graphQL.test.test_testcase
# Create your tests here.
class TestcasesTest(GraphQLTestCase):
    def test_get_testcases_query(self):
        response = self.query(
            '''
            query 
                {
                    testCases(experimentId: "6438f6ea0b7e9d05970def5a") {
                        id
                        name
                        description
                        dynamicVarValues {
                        key
                        value
                        }
                        experimentId
                        expectedResult
                        updatedAt
                        createdAt
                    }
                }
            '''      
          )

        content = json.loads(response.content)

        # This validates the status code and if you get errors
        self.assertResponseNoErrors(response)
      
        # Add some more asserts if you like
      
    def test_create_testcase_mutation(self):
        response = self.query(
            '''
            mutation {
                createTestCases(testCaseData:{
                    experimentId:"6438f6ea0b7e9d05970def5a",
                    name:"new Testcase",
                    dynamicVarValues:{key:"hey",value:"value"},
                    expectedResult:["hey","hey10"]}
                ) {
                    testCase {
                    id
                    name
                    description
                    expectedResult
                    dynamicVarValues {
                        key
                        value
                    }
                    createdAt
                    updatedAt
                    experimentId
                    }
                }
            }
            '''
        )

        content = json.loads(response.content)
        print('################################################\n')
        # This validates the status code and if you get errors
        self.assertResponseNoErrors(response)
        self.assertEqual(content['data']['createTestCases']['testCase']['name'], 'new Testcase')

    
    def test_create_testcase_mocked_mutations(self):
        response = self.query(
            '''
            mutation {
                createTestCases(testCaseData:{
                    name:"new Testcase",
                    dynamicVarValues:{key:"hey",value:"value"},
                    expectedResult:["hey","hey10"]}
                ) {
                    testCase {
                    id
                    name
                    description
                    expectedResult
                    dynamicVarValues {
                        key
                        value
                    }
                    createdAt
                    updatedAt
                    experimentId
                    }
                }
            }
            '''
        )

        content = json.loads(response.content)
        # This validates the status code and if you get errors
        self.assertResponseHasErrors(response)
        self.assertEqual(content['errors'][0]['message'], "Field 'TestCaseInput.experimentId' of required type 'ID!' was not provided.")
        
    
    def test_create_testcase_invalid_params(self):
        response = self.query(
            '''
            mutation {
                createTestCases(testCaseData:{
                    experimentId:"6438f6ea0b7e9d05970oef5a",
                    name:"new Testcase",
                    dynamicVarValues:{key:"hey",value:"value"},
                    expectedResult:["hey","hey10"]}
                ) {
                    testCase {
                    id
                    name
                    description
                    expectedResult
                    dynamicVarValues {
                        key
                        value
                    }
                    createdAt
                    updatedAt
                    experimentId
                    }
                }
            }
            '''
        )

        content = json.loads(response.content)
        # This validates the status code and if you get errors
        self.assertResponseHasErrors(response)
        self.assertEqual(content['errors'][0]['message'], 'Something went wrong')
        self.assertEqual(content['errors'][0]['extensions']['code'],'m_b_1')
        self.assertEqual(content['errors'][0]['extensions']['debug'],'Something went wrong')
        self.assertEqual(content['data']['createTestCases'],None)

        