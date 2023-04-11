import graphene
from django.core.exceptions import ObjectDoesNotExist
from .models import Experiment
from .types import ExperimentType

class CreateExperimentMutation(graphene.Mutation):
    class Arguments:
        name = graphene.String()
        description = graphene.String()

    experiment = graphene.Field(ExperimentType)

    def mutate(root, info, name, description):
        experiment = Experiment(name=name, description=description)
        experiment.save()
        return CreateExperimentMutation(experiment=experiment)
