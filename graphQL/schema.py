import graphene
from graphene.relay import Node
from .mutations import CreateExperimentMutation, CreateExampleMutation, UpdateExperimentMutation, CreatePromptTemplateMutation, UpdatePromptTemplateMutation
from .models import Experiment
from .types import ExperimentType, ExampleType , PromptTemplateType, ExperimentPaginationType



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
    experiments_by_pagination = graphene.List(ExperimentType, limit=graphene.Int(required=True), page=graphene.Int())
    experiments_by_pagination_count = graphene.Field(ExperimentPaginationType, limit=graphene.Int(required=True), page=graphene.Int())

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
        limit = kwargs.get('limit')
        page = kwargs.get('page', 0)
        offset = page * limit
        return Experiment.objects[offset:offset+limit]
    
    def resolve_experiments_by_pagination_count(self, info, **kwargs):
        limit = kwargs.get('limit')
        page = kwargs.get('page', 0)
        offset = page * limit
        
        total_count = Experiment.objects.count()
        experiments = Experiment.objects[offset:offset+limit]

        return ExperimentPaginationType(total_count=total_count, items=experiments)

    
schema = graphene.Schema(query=Query, mutation=Mutations, types=[ExperimentType, ExampleType, PromptTemplateType])
print(schema)


