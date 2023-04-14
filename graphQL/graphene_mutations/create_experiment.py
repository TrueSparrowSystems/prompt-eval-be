import graphene
from graphQL.db_models.experiment import Experiment
from graphQL.graphene_types.experiment import ExperimentType
from .mutation_base import MutateBase

        
class CreateExperimentMutation(MutateBase):
    class Arguments:
        name = graphene.String(required=True)
        description = graphene.String()

    experiment = graphene.Field(ExperimentType)

    @staticmethod
    def self_mutate(root, info, name, **kwargs):
        experiment = Experiment(name=name)
        if 'description' in kwargs:
            experiment.description = kwargs['description']

        experiment.save()
        return CreateExperimentMutation(experiment=experiment)