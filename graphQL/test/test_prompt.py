import json
from graphene_django.utils.testing import GraphQLTestCase
from graphQL.db_models.experiment import Experiment
from graphQL.db_models.prompt_template import PromptTemplate

# Command to run test cases for experiment
# $ python manage.py test graphQL.test.test_prompt
# Create your tests here.
class PromptTest(GraphQLTestCase):

    def test_create_prompt_mutation(self):
        experiment = Experiment.objects.create(name="Test Experiment", description="This is a test experiment")
        variables = {"experimentId": str(experiment.id)}       
        response = self.query(
            '''
            mutation createPromptTemplate($experimentId: ID!) {
            createPromptTemplate(
                promptTemplateData:{
                    name:"Test Prompt",
                    description:"This is a test prompt",
                    experimentId: $experimentId,
                    conversation:[{role:"system",content:"newone"}]
                    }
                ) {
                promptTemplate{
                id
                name
                description
                conversation{
                    role
                    content
                    }
                createdAt
                updatedAt
                }
             }
            }
            ''', variables=variables
        )

        content = json.loads(response.content)
        # This validates the status code and if you get errors
        self.assertResponseNoErrors(response)
        self.assertEqual(content['data']['createPromptTemplate']['promptTemplate']['name'], 'Test Prompt')
        self.assertEqual(content['data']['createPromptTemplate']['promptTemplate']['description'], 'This is a test prompt')

        Experiment.objects.filter(id=str(experiment.id)).delete()
        PromptTemplate.objects.filter(id=str(content['data']['createPromptTemplate']['promptTemplate']['id'])).delete()

        # Add some more asserts if you like
    def test_get_prompts_by_experiment_id(self):
        experiment = Experiment.objects.create(name="Test Experiment", description="This is a test experiment")
        variables = {'experimentId': str(experiment.id)}  
        response = self.query(
            '''
            query getPromptListByExperimentId($experimentId: String!) {
                    promptListByPagination(experimentId: $experimentId , limit:2, page:1){
                        totalCount
                        prompts{
                        id
                        name
                        description
                        conversation{
                            role
                            content
                        }
                        createdAt
                        updatedAt
                        }
                    }
                }
             
            ''', variables=variables
          )

        content = json.loads(response.content)

        # This validates the status code and if you get errors
        self.assertResponseNoErrors(response)
        Experiment.objects.filter(id=str(experiment.id)).delete()
      
        # Add some more asserts if you like
        
    # Write test case for create prompt mutation having length of name greater than 70 characters also compare error dictionary with expcted dictionary
    def test_create_prompt_mutation_invalid_length(self):
        experiment = Experiment.objects.create(name="Test Experiment", description="This is a test experiment")
        variables = {'experimentId': str(experiment.id)}  
        response = self.query(
            '''
            mutation createPromptTemplate($experimentId: ID!) {
            createPromptTemplate(
                promptTemplateData:{
                    name:"Test Prompt Test Prompt Test Prompt Test Prompt Test Prompt Test Prompt Test Prompt Test Prompt",
                    description:"This is a test prompt",
                    experimentId:$experimentId,
                    conversation:[{role:"system",content:"newone"}]
                    }
                ) {
                promptTemplate{
                id
                name
                description
                conversation{
                    role
                    content
                    }
                createdAt
                updatedAt
                }
             }
            }
            ''', variables=variables
        )

        content = json.loads(response.content)
        # This validates the status code and if you get errors
        self.assertResponseHasErrors(response)
        # assert equal error dictionary with expected dictionary
         # assert equal error dictionary with expected dictionary
        print('--------------------------######_----------',content)
        self.assertEqual(content['errors'][0]['message'], 'Invalid length')
        self.assertEqual(content['errors'][0]['path'][0], 'createPromptTemplate')
        self.assertEqual(content['errors'][0]['locations'][0]['line'], 3)
        self.assertEqual(content['errors'][0]['locations'][0]['column'], 13)

        Experiment.objects.filter(id=str(experiment.id)).delete()


    def test_update_prompt_mutaion(self):
        experiment = Experiment.objects.create(name="Test Experiment", description="This is a test experiment")
        prompt = PromptTemplate.objects.create(experiment_id=str(experiment.id),name="Test Prompt", description="This is a test prompt")
        variables = {"promptId": str(prompt.id)}
        response = self.query(
            '''
            mutation updatePromptTemplate($promptId: String!) {
            updatePromptTemplate(
                updatePromptTemplateData:{
                    id:$promptId,
                    name:"Test Prompt",
                    description:"This is a test prompt"
                    }
                ) {
                promptTemplate{
                id
                name
                description
                conversation{
                    role
                    content
                    }
                createdAt
                updatedAt
                }
             }
            }
            ''', variables=variables
        )
        content = json.loads(response.content)
        # This validates the status code and if you get errors
        self.assertResponseNoErrors(response)
        self.assertEqual(content['data']['updatePromptTemplate']['promptTemplate']['name'], 'Test Prompt')
        self.assertEqual(content['data']['updatePromptTemplate']['promptTemplate']['description'], 'This is a test prompt')

        Experiment.objects.filter(id=str(experiment.id)).delete()
        PromptTemplate.objects.filter(id=str(prompt.id)).delete()

        # Add some more asserts if you like

    def test_update_prompt_mutaion_invalid_length(self):
        experiment = Experiment.objects.create(name="Test Experiment", description="This is a test experiment")
        prompt = PromptTemplate.objects.create(experiment_id=str(experiment.id),name="Test Prompt", description="This is a test prompt")
        variables = {"promptId": str(prompt.id)}
        response = self.query(
            '''
            mutation updatePromptTemplate($promptId: String!) {
            updatePromptTemplate(
                updatePromptTemplateData:{
                    id:$promptId,
                    name:"Test Prompt Test Prompt Test Prompt Test Prompt Test Prompt Test Prompt Test Prompt Test Prompt",
                    description:"This is a test prompt",
                    conversation:[{role:"system",content:"newone"}]
                    }
                ) {
                promptTemplate{
                id
                name
                description
                conversation{
                    role
                    content
                    }
                createdAt
                updatedAt
                }
             }
            }
            ''', variables=variables
        )

        content = json.loads(response.content)
        # This validates the status code and if you get errors
        self.assertResponseHasErrors(response)
        # assert equal error dictionary with expected dictionary
         # assert equal error dictionary with expected dictionary
        print('--------------------------######_----------',content)
        self.assertEqual(content['errors'][0]['message'], 'Invalid length')
        self.assertEqual(content['errors'][0]['path'][0], 'updatePromptTemplate')
        self.assertEqual(content['errors'][0]['locations'][0]['line'], 3)
        self.assertEqual(content['errors'][0]['locations'][0]['column'], 13)

        Experiment.objects.filter(id=str(experiment.id)).delete()
        PromptTemplate.objects.filter(id=str(prompt.id)).delete()




        
      
    