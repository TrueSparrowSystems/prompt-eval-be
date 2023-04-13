import graphene
from graphene.relay import Node, Connection
from graphene_mongo.fields import MongoengineConnectionField
from .mutations import CreateExperimentMutation, CreateExampleMutation, UpdateExperimentMutation, CreatePromptTemplateMutation, UpdatePromptTemplateMutation
from .models import Experiment
from .types import ExperimentType, ExampleType , ExperimentConnection , PromptTemplateType


class Mutations(graphene.ObjectType):
    create_experiment = CreateExperimentMutation.Field()
    create_example = CreateExampleMutation.Field()
    update_experiment = UpdateExperimentMutation.Field()
    create_prompt_template = CreatePromptTemplateMutation.Field()
    update_prompt_template = UpdatePromptTemplateMutation.Field()
    
class Query(graphene.ObjectType):
    node = Node.Field()
    experiment_list = graphene.List(ExperimentType, name=graphene.String())
    experiment_list_by_id = graphene.Field(ExperimentType, documentId=graphene.String(required=True))
    experiments_by_pagination = MongoengineConnectionField(ExperimentType)

    def resolve_experiment_list(root, info, name=None):
        if name:
            return Experiment.objects.filter(name=name)            
        else:
            return Experiment.objects.all()
            
    def resolve_experiment_list_by_id(self, info, documentId=graphene.String(required=True)):
        try:
            return Experiment.objects.get(_id=documentId)
        except Experiment.DoesNotExist:
            return None
    
    def resolve_experiments_by_pagination(self, info, **kwargs):
        try:
            queryset = Experiment.objects.order_by('id')
            return queryset
        except queryset.DoesNotExist:
            return None

    
schema = graphene.Schema(query=Query, mutation=Mutations, types=[ExperimentType, ExampleType, ExperimentConnection, PromptTemplateType])

