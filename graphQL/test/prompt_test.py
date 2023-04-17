import json
from graphene_django.utils.testing import GraphQLTestCase

# Command to run test cases for experiment
# $ python manage.py test graphQL.test.prompt_experiment
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
                experimentId: "643d4e97c865c10095c972e5"
                name: "Prompt 6"
                description: "desc of Sixth one"
                conversation: [{role: "SYSTEM", content: "I'm chat"}, {role: "USER", content: "I know chat"},{role:"ASSISTENT", content:"BYE"}]
            ) {
                promptTemplate {
                id
                name
                description
                createdAt
                updatedAt
                conversation {
                    role
                    content
                }
                }
            }
            }
            '''
        )

        content = json.loads(response.content)
        print('################################################\n')
        # This validates the status code and if you get errors
        self.assertResponseNoErrors(response)
        # self.assertEqual(content['data']['createPromptTemplate']['prompt']['name'], 'Test Prompt')
        # self.assertEqual(content['data']['createPromptTemplate']['prompt']['description'], 'This is a test prompt')

        # Add some more asserts if you like
      
    