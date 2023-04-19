import json
from graphene_django.utils.testing import GraphQLTestCase

# Command to run test cases for experiment
# $ python manage.py test graphQL.test.test_prompt
# Create your tests here.
class PromptTest(GraphQLTestCase):
    def test_get_prompts_by_experiment_id(self):
        response = self.query(
            '''
            query {
                    promptListByPagination(experimentId:"643d4e97c865c10095c972e5", limit:2, page:1){
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
             
            '''      
          )

        content = json.loads(response.content)

        # This validates the status code and if you get errors
        self.assertResponseNoErrors(response)
      
        # Add some more asserts if you like
        
    def test_create_prompt_mutation(self):
        response = self.query(
            '''
            mutation {
            createPromptTemplate(
                promptTemplateData:{
                    name:"Test Prompt",
                    description:"This is a test prompt",
                    experimentId:"643d4e97c865c10095c972e5",
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
            '''
        )

        content = json.loads(response.content)
        # This validates the status code and if you get errors
        self.assertResponseNoErrors(response)
        self.assertEqual(content['data']['createPromptTemplate']['promptTemplate']['name'], 'Test Prompt')
        self.assertEqual(content['data']['createPromptTemplate']['promptTemplate']['description'], 'This is a test prompt')

        # Add some more asserts if you like
        
    # Write test case for create prompt mutation having length of name greater than 70 characters also compare error dictionary with expcted dictionary
    def test_create_prompt_mutation_invalid_length(self):
        response = self.query(
            '''
            mutation {
            createPromptTemplate(
                promptTemplateData:{
                    name:"Test Prompt Test Prompt Test Prompt Test Prompt Test Prompt Test Prompt Test Prompt Test Prompt",
                    description:"This is a test prompt",
                    experimentId:"643d4e97c865c10095c972e5",
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
            '''
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

        
        
      
    