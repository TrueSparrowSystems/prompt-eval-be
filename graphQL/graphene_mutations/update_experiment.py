import graphene
import time
from graphQL.db_models.experiment import Experiment
from graphQL.graphene_types.experiment import ExperimentType
from .mutation_base import MutateBase

class UpdateExperimentMutation(MutateBase):
    class Arguments:
        documentId = graphene.String(required=True)
        name = graphene.String() 
        description = graphene.String()
        dynamic_vars = graphene.List(graphene.String)

    experiment = graphene.Field(ExperimentType)

    @staticmethod
    def self_mutate(root, info,documentId, **kwargs):
        experiment = Experiment.objects.get(id=documentId)

        if 'name' in kwargs:
            experiment.name = kwargs['name']
            
        if 'description' in kwargs:
            experiment.description = kwargs['description']
        
        if 'dynamic_vars' in kwargs:
            experiment.dynamic_vars = kwargs['dynamic_vars']
       
        experiment.updated_at = int(time.time())
        experiment.save()
        return UpdateExperimentMutation(experiment=experiment)