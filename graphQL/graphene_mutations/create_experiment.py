import graphene
from graphQL.db_models.experiment import Experiment
from graphQL.graphene_types.experiment import ExperimentType
from .mutation_base import MutateBase
from graphQL.lib.helper import CommonValiator
from graphQL.lib.custom_exception import InvalidLengthError

from bg_jobs.background_job import background_job
from bg_jobs.executor import executor

class ExperimentInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    description = graphene.String()
    
class CreateExperimentMutation(MutateBase):
    class Arguments:
        experiment_data = ExperimentInput(required=True)

    experiment = graphene.Field(ExperimentType)

    @classmethod
    def self_mutate(cls, root, info, experiment_data=None):
        if not CommonValiator.max_length_validation(experiment_data.name, 70):
            raise InvalidLengthError(code = "g_gm_ce_1", param="name")

        experiment = Experiment(name=experiment_data.name)
        if experiment_data.description:
            if not CommonValiator.max_length_validation(experiment_data.description, 240):
                raise InvalidLengthError(code = "g_gm_ce_2", param="description")
            experiment.description = experiment_data.description

        experiment.save()
        
        for i in range(5):
            params = {'p1': i, 'p2': i+1}
            executor.submit(background_job, params)
        print('Main thread execution done, bg is still processing')
    

        return CreateExperimentMutation(experiment=experiment)