import json
from graphene_django.utils.testing import GraphQLTestCase

# Command to run test cases for experiment
# $ python manage.py test graphQL.test.test_report
# Create your tests here.

class ReportTest(GraphQLTestCase):
    def test_get_report_query(self):
        response = self.query(
            '''
            query {
                getReport(reportId:"64410b5c8402313be9d1f85e",page:1,limit:2){
                    id
                    model
                    eval
                    accuracy
                    promptTemplateId
                    runId
                    status
                    initiatedAt
                    completedAt
                    createdAt
                    updatedAt
                    testCaseEvaluationReport{
                        id
                        evaluationResultId
                        prompt
                        testCaseId
                        testCaseName
                        testCaseDescription
                        actualResult
                        acceptableResult
                        accuracy
                    }
                }
                }
            '''      
          )

        content = json.loads(response.content)

        # This validates the status code and if you get errors
        self.assertResponseNoErrors(response)
      
        # Add some more asserts if you like
    def test_get_report_query_with_invalid_id(self):
        response = self.query(
            '''
            query {
                getReport(reportId:1123,page:1,limit:2){
                    id
                    model
                    eval
                    accuracy
                    promptTemplateId
                    runId
                    status
                    initiatedAt
                    completedAt
                    createdAt
                    updatedAt
                    testCaseEvaluationReport{
                        id
                        evaluationResultId
                        prompt
                        testCaseId
                        testCaseName
                        testCaseDescription
                        actualResult
                        acceptableResult
                        accuracy
                    }
                }
                }
            '''      
          )

        content = json.loads(response.content)

        # This validates the status code and if you get errors
        self.assertResponseHasErrors(response)
        self.assertEqual(content['errors'][0]['message'], 'String cannot represent a non string value: 1123')
      
        # Add some more asserts if you like
    
    def test_get_report_query_with_invalid_page(self):
        response = self.query(
            '''
            query {
                getReport(reportId:"64410b5c8402313be9d1f85e",page:-1,limit:2){
                    id
                    model
                    eval
                    accuracy
                    promptTemplateId
                    runId
                    status
                    initiatedAt
                    completedAt
                    createdAt
                    updatedAt
                    testCaseEvaluationReport{
                        id
                        evaluationResultId
                        prompt
                        testCaseId
                        testCaseName
                        testCaseDescription
                        actualResult
                        acceptableResult
                        accuracy
                    }
                }
                }
            '''      
          )

        content = json.loads(response.content)

        # This validates the status code and if you get errors
        self.assertResponseHasErrors(response)
        self.assertEqual(content['errors'][0]['message'], 'Something went wrong')
        self.assertEqual(content['errors'][0]['extensions']['code'], 'g_s_q_r_4')
        self.assertEqual(content['errors'][0]['extensions']['debug'], 'Something_went_wrong')
        self.assertEqual(content['data']['getReport'], None)
        # Add some more asserts if you like

    def test_get_report_query_with_invalid_limit(self):
        response = self.query(
            '''
            query {
                getReport(reportId:"64410b5c8402313be9d1f85e",page:1,limit:-1){
                    id
                    model
                    eval
                    accuracy
                    promptTemplateId
                    runId
                    status
                    initiatedAt
                    completedAt
                    createdAt
                    updatedAt
                    testCaseEvaluationReport{
                        id
                        evaluationResultId
                        prompt
                        testCaseId
                        testCaseName
                        testCaseDescription
                        actualResult
                        acceptableResult
                        accuracy
                    }
                }
                }
            '''      
          )

        content = json.loads(response.content)

        # This validates the status code and if you get errors
        self.assertResponseHasErrors(response)
        self.assertEqual(content['errors'][0]['message'], 'Something went wrong')
        self.assertEqual(content['errors'][0]['extensions']['code'], 'g_s_q_r_4')
        self.assertEqual(content['errors'][0]['extensions']['debug'], 'Something_went_wrong')
        self.assertEqual(content['data']['getReport'], None)
      
        # Add some more asserts if you like

    def test_get_report_query_with_invalid_page_and_limit(self):
        response = self.query(
            '''
            query {
                getReport(reportId:"64410b5c8402313be9d1f85e",page:-1,limit:-1){
                    id
                    model
                    eval
                    accuracy
                    promptTemplateId
                    runId
                    status
                    initiatedAt
                    completedAt
                    createdAt
                    updatedAt
                    testCaseEvaluationReport{
                        id
                        evaluationResultId
                        prompt
                        testCaseId
                        testCaseName
                        testCaseDescription
                        actualResult
                        acceptableResult
                        accuracy
                    }
                }
                }
            '''      
          )

        content = json.loads(response.content)

        # This validates the status code and if you get errors
        self.assertResponseHasErrors(response)
        self.assertEqual(content['errors'][0]['message'], 'Something went wrong')
        self.assertEqual(content['errors'][0]['extensions']['code'], 'g_s_q_r_4')
        self.assertEqual(content['errors'][0]['extensions']['debug'], 'Something_went_wrong')
        self.assertEqual(content['data']['getReport'], None)
      
        # Add some more asserts if you like
