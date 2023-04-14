import graphene
import time
from django.core.exceptions import ObjectDoesNotExist
from .models import Experiment, Example, PromptTemplate
from .types import ExperimentType, ExampleType, PromptTemplateType, InputConversationType
from graphql import GraphQLError

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
    
class MutateBase(graphene.Mutation):

    @staticmethod
    def self_mutate(root, info, **kwargs):
        raise NotImplementedError('self_mutate must be implemented to use MutateBase')
    
    @classmethod
    def mutate(cls,root, info, **kwargs):
        try:
            return cls.self_mutate(root, info, **kwargs)
        except Exception as e:
            print(e)
            error = GraphQLError(
            message="Something went wrong",
            extensions= {
             "code": "m_b_1",
             "debug": "Something_went_wrong",
             }
            )
            return error
    
    
class UpdatePromptTemplateMutation(MutateBase):
    class Arguments:
        documentId = graphene.String(required=True)
        description = graphene.String()

    promptTemplate = graphene.Field(PromptTemplateType)

    @staticmethod
    def self_mutate(root, info, documentId, description):
        print(documentId)
        query = promptTemplate = PromptTemplate.objects.get(_id=documentId)
        print('Mongoengine queries 1')
        print(str(query.to_mongo()))
        promptTemplate.description = description
        query = promptTemplate.save()
        print('Mongoengine queries 2')
        print(str(query.to_mongo()))
        return UpdatePromptTemplateMutation(promptTemplate=promptTemplate)
    
     

  


