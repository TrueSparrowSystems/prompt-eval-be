import json
from graphene_django.utils.testing import GraphQLTestCase
from graphQL.db_models.experiment import Experiment
from graphQL.db_models.prompt_template import PromptTemplate
from graphQL.db_models.evaluation import Evaluation

# Command to run test cases for experiment
# $ python manage.py test graphQL.test.test_report
# Create your tests here.

class ReportTest(GraphQLTestCase):
    def test_get_report_query(self):
        experiment = Experiment.objects.create(name="Test Experiment", description="This is a test experiment")
        prompt = PromptTemplate.objects.create(experiment_id=str(experiment.id),name="Test Prompt", description="This is a test prompt")
        evaluation = Evaluation.objects.create(prompt_template_id=str(prompt.id),model="Test Model",eval="Test Eval")
        variables = {"reportID": str(evaluation.id)}
        response = self.query(
            '''
            query getReport($reportID:String!){
                getReport(reportId:$reportID,page:1,limit:2){
                    id
                    model
                    eval
                    accuracy
                    totalTestcases
                    passedTestcases
                    promptTemplateId
                    runId
                    status
                    initiatedAt
                    completedAt
                    createdAt
                    updatedAt
                    testCaseEvaluationReport{
                        id
                        prompt{
                            role,
                            content
                        }
                        testCaseId
                        testCaseName
                        testCaseDescription
                        actualResult
                        acceptableResult
                        accuracy
                    }
                }
                }
            '''  , variables=variables    
          )

        content = json.loads(response.content)
        print('----------------------content----------------------',content)
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
                    totalTestcases
                    passedTestcases
                    promptTemplateId
                    runId
                    status
                    initiatedAt
                    completedAt
                    createdAt
                    updatedAt
                    testCaseEvaluationReport{
                        id
                        prompt{
                            role,
                            content
                        }
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
                    totalTestcases
                    passedTestcases
                    promptTemplateId
                    runId
                    status
                    initiatedAt
                    completedAt
                    createdAt
                    updatedAt
                    testCaseEvaluationReport{
                        id
                        prompt{
                            role,
                            content
                        }
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
                    totalTestcases
                    passedTestcases
                    promptTemplateId
                    runId
                    status
                    initiatedAt
                    completedAt
                    createdAt
                    updatedAt
                    testCaseEvaluationReport{
                        id
                        prompt{
                            role,
                            content
                        }
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
                        prompt{
                            role,
                            content
                        }
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
