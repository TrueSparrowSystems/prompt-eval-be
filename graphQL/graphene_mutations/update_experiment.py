import graphene
import time
from graphQL.db_models.experiment import Experiment
from graphQL.graphene_types.experiment import ExperimentType
from .mutation_base import MutateBase
from graphQL.lib.helper import CommonValidator
from graphQL.lib.custom_exception import InvalidLengthError

class UpdateExperimentInput(graphene.InputObjectType):
    id = graphene.String(required=True)
    name = graphene.String()
    description = graphene.String()
    dynamic_vars = graphene.List(graphene.String)

class UpdateExperimentMutation(MutateBase):
    class Arguments:
        update_experiment_data = UpdateExperimentInput(required=True)

    experiment = graphene.Field(ExperimentType)

    """
    update experiment

    @params {Object} update_experiment_data
    @params {String} update_experiment_data.id
    @params {String} update_experiment_data.name
    @params {String} update_experiment_data.description
    @params {String} update_experiment_data.dynamic_vars

    @returns {Object} UpdateExperimentMutation object
    """
    @classmethod
    def self_mutate(cls, root, info, update_experiment_data=None):
        experiment = Experiment.objects.get(id=update_experiment_data.id)

        if update_experiment_data.name:
            if not CommonValidator.max_length_validation(update_experiment_data.name, 70):
                raise InvalidLengthError(code = "g_gm_ue_1", param="name")
            experiment.name = update_experiment_data.name

        if update_experiment_data.description:
            if not CommonValidator.max_length_validation(update_experiment_data.description, 240):
                raise InvalidLengthError(code = "g_gm_ue_2", param="description")
            experiment.description = update_experiment_data.description

        if update_experiment_data.dynamic_vars:
            experiment.dynamic_vars = update_experiment_data.dynamic_vars

        experiment.save()
        return UpdateExperimentMutation(experiment=experiment)