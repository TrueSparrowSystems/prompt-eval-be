import graphene
from django.core.exceptions import ObjectDoesNotExist
from .models import Experiment, Example
from .types import ExperimentType, ExampleType

class CreateExperimentMutation(graphene.Mutation):
    class Arguments:
        name = graphene.String()
        description = graphene.String()

    experiment = graphene.Field(ExperimentType)

    def mutate(root, info, name, description):
        experiment = Experiment(name=name, description=description)
        experiment.save()
        # print(experiment.name)
        # print(experiment.description)
        # print(experiment)
        # for key, value in vars(experiment).items():
        #     print(f"{key}: {value}")
        # print(experiment._cls)
        # print(experiment.auto_id_0)
        return CreateExperimentMutation(experiment=experiment)
    
class UpdateExperimentMutation(graphene.Mutation):
    class Arguments:
        documentId = graphene.String(required=True)
        name = graphene.String() 
        description = graphene.String()

    experiment = graphene.Field(ExperimentType)

    def mutate(root, info, documentId, name, description):
        try:
            experiment = Experiment.objects.get(_id=documentId)
        except ObjectDoesNotExist:
            return None
        experiment.name = name
        experiment.description = description
        experiment.save()
        return UpdateExperimentMutation(experiment=experiment)
    
class CreateExampleMutation(graphene.Mutation):
    class Arguments:
        name = graphene.String()
        description = graphene.String()

    example = graphene.Field(ExampleType)

    def mutate(root, info, name, description):
        example = Example(name=name, description=description)
        example.save()
        print(example.name)
        print(example.description)
        print(example)
        return CreateExampleMutation(example=example)
