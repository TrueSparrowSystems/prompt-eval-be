import graphene
import time
from django.core.exceptions import ObjectDoesNotExist
from .models import Experiment, Example, PromptTemplate
from .types import ExperimentType, ExampleType, PromptTemplateType, InputConversationType


class CreateExperimentMutation(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        description = graphene.String()

    experiment = graphene.Field(ExperimentType)

    def mutate(root, info, name, **kwargs):
        experiment = Experiment(name=name)
        if 'description' in kwargs:
            experiment.description = kwargs['description']

        experiment.save()
        return CreateExperimentMutation(experiment=experiment)
    
class UpdateExperimentMutation(graphene.Mutation):
    class Arguments:
        documentId = graphene.String(required=True)
        name = graphene.String() 
        description = graphene.String()
        dynamic_vars = graphene.List(graphene.String)

    experiment = graphene.Field(ExperimentType)

    def mutate(root, info,documentId, **kwargs):
        experiment = Experiment.objects.get(id=documentId)

        fields = {}
        for arg_name, arg_value in kwargs.items():
            if arg_name in ['name', 'description','dynamic_vars']:
                fields[arg_name] = arg_value
        experiment.update(**fields)
        experiment.updated_at = int(time.time())
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
        name = graphene.String(required=True)
        description = graphene.String()
        conversation = graphene.List(InputConversationType)
        experimentId = graphene.ID(required=True)

    promptTemplate = graphene.Field(PromptTemplateType)

    def mutate(root, info, name,experimentId, **kwargs):

        fields = {}
        for arg_name, arg_value in kwargs.items():
            if arg_name in ['description', 'conversation']:
                fields[arg_name] = arg_value
        
        promptTemplate = PromptTemplate(name=name, experiment_id=experimentId, **fields)
        promptTemplate.save()

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

  


