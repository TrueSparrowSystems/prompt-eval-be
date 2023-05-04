import json
from graphene_django.utils.testing import GraphQLTestCase
from graphQL.db_models.experiment import Experiment

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
        self.assertEqual(content['data']['createExperiment']
                         ['experiment']['name'], 'Test Experiment')
        self.assertEqual(content['data']['createExperiment']
                         ['experiment']['description'], 'This is a test experiment')
        
        Experiment.objects.filter(id=content['data']['createExperiment']['experiment']['id']).delete()

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
        experiment = Experiment.objects.create(name="Test Experiment", description="This is a test experiment")
        variables = {'documentId': str(experiment.id)}
        response = self.query(
            '''
            mutation updateExperiment(
                $documentId: String!
            ) {
                updateExperiment(
                updateExperimentData: {
                    name: "Updated Experiment"
                    id: $documentId
                    description: "new description"
                }
                ) {
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
            ''', variables=variables
        )

        content = json.loads(response.content)

        # This validates the status code and if you get errors
        self.assertResponseNoErrors(response)
        Experiment.objects.filter(id=experiment.id).delete()
        # Add some more asserts if you like

    def test_update_experiment_mocked_mutation(self):
        experiment = Experiment.objects.create(name="Test Experiment", description="This is a test experiment")
        variables = {'id': str(experiment.id)}
        response = self.query(
            '''
            mutation UpdateExperiment($id: String!) {
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
            ''', variables=variables
        )

        content = json.loads(response.content)
        print('Content data--------', content)

        # This validates the status code and if you get errors
        self.assertResponseHasErrors(response)
        Experiment.objects.filter(id=experiment.id).delete()
        # Add some more asserts if you like

    def test_update_experiment_with_incorrect_id(self):
        response = self.query(
            '''
            mutation UpdateExperiment($id: String!) {
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
