import graphene
from graphQL.graphene_mutations.create_experiment import CreateExperimentMutation
from graphQL.graphene_mutations.update_experiment import UpdateExperimentMutation
from graphQL.graphene_mutations.create_prompt_template import CreatePromptTemplateMutation
from graphQL.graphene_mutations.create_test_cases import CreateTestCasesMutation
from graphQL.db_models.experiment import Experiment
from graphQL.db_models.prompt_template import PromptTemplate
from graphQL.db_models.test_case import TestCase
from graphQL.graphene_types.experiment import ExperimentType, ExperimentPaginationType
from graphQL.graphene_types.prompt_template import PromptTemplateType, PromptTemplatePaginationType
from graphQL.graphene_types.test_case import TestCaseType
from graphql import GraphQLError

class Mutations(graphene.ObjectType):
    create_experiment = CreateExperimentMutation.Field()
    update_experiment = UpdateExperimentMutation.Field()
    create_prompt_template = CreatePromptTemplateMutation.Field()
    create_test_cases = CreateTestCasesMutation.Field()

    
class Query(graphene.ObjectType):
    experiment_list = graphene.List(ExperimentType)
    prompt_list_by_pagination = graphene.Field(PromptTemplatePaginationType, experimentId=graphene.String(required=True), limit=graphene.Int(required=True), page=graphene.Int(required=True))
    test_cases = graphene.List(TestCaseType, experimentId=graphene.String(required=True))

    def resolve_experiment_list(root, info): 
        try:
            return Experiment.objects.all()
        except Exception as e:
            print(e)
            error = GraphQLError(
            message="Something went wrong",
            extensions= {
             "code": "g_s_q_r_1",
             "debug": "Something_went_wrong",
             }
            )
            return error    
    
    def resolve_prompt_list_by_pagination(self, info, experimentId=graphene.String(required=True), **kwargs):
        try:
            limit = kwargs.get('limit')
            page = kwargs.get('page')
            offset = (page - 1) * limit
            
            total_count = PromptTemplate.objects.filter(experiment_id=experimentId).count()
            prompts = PromptTemplate.objects.filter(experiment_id=experimentId).order_by('-updated_at')[offset:offset+limit]

            return PromptTemplatePaginationType(total_count=total_count, prompts=prompts)
        except Exception as e:
            print(e)
            error = GraphQLError(
            message="Something went wrong",
            extensions= {
             "code": "g_s_q_r_2",
             "debug": "Something_went_wrong",
             }
            )
            return error
            

    def resolve_test_cases(self, info, experimentId=graphene.String(required=True)):
        try:
            return TestCase.objects.filter(experiment_id=experimentId)
        except Exception as e:
            print(e)
            error = GraphQLError(
            message="Something went wrong",
            extensions= {
             "code": "g_s_q_r_3",
             "debug": "Something_went_wrong",
             }
            )
            return error

    
schema = graphene.Schema(query=Query, mutation=Mutations, types=[ExperimentType, PromptTemplateType, ExperimentPaginationType])


