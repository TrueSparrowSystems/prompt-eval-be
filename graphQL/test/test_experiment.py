import json
from graphene_django.utils.testing import GraphQLTestCase

# Command to run test cases for experiment
# $ python manage.py test graphQL.test.test_experiment
# Create your tests here.
class ExperimentTest(GraphQLTestCase):
    def test_get_experiments_query(self):
        response = self.query(
            '''
            query {
                experimentList {
                    id
                    name
                    description
                    createdAt
                    updatedAt
                    dynamicVars
                }
            }
            '''      
          )

        content = json.loads(response.content)

        # This validates the status code and if you get errors
        self.assertResponseNoErrors(response)
      
        # Add some more asserts if you like
      
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
        self.assertEqual(content['data']['createExperiment']['experiment']['name'], 'Test Experiment')
        self.assertEqual(content['data']['createExperiment']['experiment']['description'], 'This is a test experiment')

    
    def test_create_experiment_mocked_mutations(self):
      response = self.query(
            '''
            mutation {
                createExperiment(experimentData:{description:"description of 1 "}) {
                    experiment {
                        id
                        name
                        description
                        createdAt
                        updatedAt
                        dynamicVars
                    }
                }
            }
            '''
        )
    
      self.assertResponseHasErrors(response)
      
    def test_update_experiment_mutation(self):
        response = self.query(
            '''
            mutation {
                updateExperiment(
                    updateExperimentData:
                        {
                            name:"Test Experiment Update",
                            id:"6438f6ea0b7e9d05970def5a"
                        }
                ) {
                    experiment{
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

        # This validates the status code and if you get errors
        self.assertResponseNoErrors(response)

        # Add some more asserts if you like
    
    def test_update_experiment_mocked_mutation(self):
        response = self.query(
            '''
            mutation {
                updateExperiment(updateExperimentData:
                    {
                    name:"Test Experiment Update",
                    description: "This is a test experiment update",
                    id:"6438f6ea0b7e9d05970def5e"
                    }
                ) {
                    experiment{
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
        print('Content data--------', content)

        # This validates the status code and if you get errors
        self.assertResponseHasErrors(response)

        # Add some more asserts if you like
        
    def test_update_experiment_with_incorrect_id(self):
        response = self.query(
            '''
            mutation {
                updateExperiment(updateExperimentData:
                    {
                    name:"Test Experiment Update",
                    description: "This is a test experiment update",
                    id:"6438f6ea0b7e9d05970def5b"
                    }
                ) {
                    experiment{
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

        # This validates the status code and if you get errors
        self.assertResponseHasErrors(response)
        # Add some more asserts if you like

    
    


      
