import graphene
from graphQL.db_models.experiment import Experiment
from graphQL.graphene_types.experiment import ExperimentType
from .mutation_base import MutateBase
from graphQL.lib.helper import CommonValiator
        
class CreateExperimentMutation(MutateBase):
    class Arguments:
        name = graphene.String(required=True)
        description = graphene.String()

    experiment = graphene.Field(ExperimentType)

    @staticmethod
    def self_mutate(root, info, name, **kwargs):
        if not CommonValiator.length_validation(name, 70):
            raise Exception('Invalid length')
    
        experiment = Experiment(name=name)
        if 'description' in kwargs:
            if not CommonValiator.length_validation(kwargs['description'], 240):
                raise Exception('Invalid length')
            experiment.description = kwargs['description']

        experiment.save()
        return CreateExperimentMutation(experiment=experiment)