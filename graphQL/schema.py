import graphene
from graphene.relay import Node
from .mutations import  CreateExampleMutation
from graphQL.graphene_mutations.create_experiment import CreateExperimentMutation
from graphQL.graphene_mutations.create_prompt_template import CreatePromptTemplateMutation
from graphQL.graphene_mutations.update_experiment import UpdateExperimentMutation
from graphQL.graphene_mutations.update_prompt_template import UpdatePromptTemplateMutation
from graphQL.db_models.experiment import Experiment
from graphQL.graphene_types.experiment import ExperimentType, ExperimentPaginationType
from graphQL.graphene_types.prompt_template import PromptTemplateType
from .types import ExampleType

class Mutations(graphene.ObjectType):
    create_experiment = CreateExperimentMutation.Field()
    update_experiment = UpdateExperimentMutation.Field()
    create_prompt_template = CreatePromptTemplateMutation.Field()
    update_prompt_template = UpdatePromptTemplateMutation.Field()
    create_example = CreateExampleMutation.Field()

    
class Query(graphene.ObjectType):
    node = Node.Field()
    experiment_list = graphene.List(ExperimentType)
    experiment_list_by_id = graphene.Field(ExperimentType, documentId=graphene.String(required=True))
    experiments_by_pagination = graphene.List(ExperimentType, limit=graphene.Int(required=True), page=graphene.Int())
    experiments_by_pagination_count = graphene.Field(ExperimentPaginationType, limit=graphene.Int(required=True), page=graphene.Int())

    def resolve_experiment_list(root, info): 
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

    
schema = graphene.Schema(query=Query, mutation=Mutations, types=[ExperimentType, ExampleType, PromptTemplateType, ExperimentPaginationType])


