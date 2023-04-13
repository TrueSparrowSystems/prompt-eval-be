import graphene
from django.core.exceptions import ObjectDoesNotExist
from .models import Experiment, Example, PromptTemplate
from .types import ExperimentType, ExampleType, PromptTemplateType


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
    
class CreatePromptTemplateMutation(graphene.Mutation):
    class Arguments:
        name = graphene.String()
        description = graphene.String()

    promptTemplate = graphene.Field(PromptTemplateType)

    def mutate(root, info, name, description):
        promptTemplate = PromptTemplate(name=name, description=description)
        promptTemplate.save()
        print(promptTemplate.name)
        print(promptTemplate.description)
        print(promptTemplate)
        for key, value in vars(promptTemplate).items():
            print(f"{key}: {value}")
        return CreatePromptTemplateMutation(promptTemplate=promptTemplate)
    
class UpdatePromptTemplateMutation(graphene.Mutation):
    class Arguments:
        documentId = graphene.String(required=True)
        description = graphene.String()

    promptTemplate = graphene.Field(PromptTemplateType)

    def mutate(root, info, documentId, description):
        try:
            print('getting id successfully')
            print(documentId)
            promptTemplate = PromptTemplate.objects.get(_id=documentId)
            print('getting id successfully')
            print(promptTemplate)
        except Exception as e:
            print('I am in except')
            print(e)
            return None
        promptTemplate.description = description
        query = promptTemplate.save()
        print('Mongoengine queries')
        print(str(query.to_mongo()))
        return UpdatePromptTemplateMutation(promptTemplate=promptTemplate)

  


