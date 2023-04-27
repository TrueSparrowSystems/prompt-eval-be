import json
from graphene_django.utils.testing import GraphQLTestCase

# Command to run test cases for experiment
# $ python manage.py test graphQL.test.test_prompt
# Create your tests here.
class PromptTest(GraphQLTestCase):
    promptID = ""
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
        PromptTest.experimentID = content['data']['createExperiment']['experiment']['id']

    def test_create_prompt_mutation(self):
        variable = {"experimentId": PromptTest.experimentID}        
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
            ''', variables=variable
        )

        content = json.loads(response.content)
        # This validates the status code and if you get errors
        self.assertResponseNoErrors(response)
        PromptTest.promptID = content['data']['createPromptTemplate']['promptTemplate']['id']
        self.assertEqual(content['data']['createPromptTemplate']['promptTemplate']['name'], 'Test Prompt')
        self.assertEqual(content['data']['createPromptTemplate']['promptTemplate']['description'], 'This is a test prompt')

        # Add some more asserts if you like
    def test_get_prompts_by_experiment_id(self):
        variable = {"experimentId": PromptTest.experimentID}
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
             
            ''', variables=variable
          )

        content = json.loads(response.content)

        # This validates the status code and if you get errors
        self.assertResponseNoErrors(response)
      
        # Add some more asserts if you like
        
    # Write test case for create prompt mutation having length of name greater than 70 characters also compare error dictionary with expcted dictionary
    def test_create_prompt_mutation_invalid_length(self):
        variable = {"experimentId": PromptTest.experimentID}
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
            ''', variables=variable
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


    def test_update_prompt_mutaion(self):
        variable = {"promptId": PromptTest.promptID}
        response = self.query(
            '''
            mutation updatePromptTemplate($promptId: String!) {
            updatePromptTemplate(
                updatePromptTemplateData:{
                    id:$promptId,
                    name:"Test Prompt",
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
            ''', variables=variable
        )

        content = json.loads(response.content)
        # This validates the status code and if you get errors
        self.assertResponseNoErrors(response)
        self.assertEqual(content['data']['updatePromptTemplate']['promptTemplate']['name'], 'Test Prompt')
        self.assertEqual(content['data']['updatePromptTemplate']['promptTemplate']['description'], 'This is a test prompt')

        # Add some more asserts if you like

    def test_update_prompt_mutaion_invalid_length(self):
        variable = {"promptId": PromptTest.promptID}
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
            ''', variables=variable
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




        
      
    