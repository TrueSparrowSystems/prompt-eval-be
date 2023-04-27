import graphene
from graphQL.graphene_mutations.create_experiment import CreateExperimentMutation
from graphQL.graphene_mutations.update_experiment import UpdateExperimentMutation
from graphQL.graphene_mutations.create_prompt_template import CreatePromptTemplateMutation
from graphQL.graphene_mutations.update_prompt_template import UpdatePromptTemplateMutation
from graphQL.graphene_mutations.create_evaluation import CreateEvaluationMutation
from graphQL.graphene_mutations.create_test_cases import CreateTestCasesMutation
from graphQL.db_models.experiment import Experiment
from graphQL.db_models.prompt_template import PromptTemplate
from graphQL.db_models.test_case import TestCase
from graphQL.db_models.evaluation import Evaluation
from graphQL.db_models.evaluation_test_case_relation import EvaluationTestCaseRelation
from graphQL.graphene_types.experiment import ExperimentType
from graphQL.graphene_types.prompt_template import PromptTemplatePaginationType
from graphQL.graphene_types.test_case import TestCaseType
from graphQL.graphene_types.report import ReportType
from graphql import GraphQLError

class Mutations(graphene.ObjectType):
    create_experiment = CreateExperimentMutation.Field()
    update_experiment = UpdateExperimentMutation.Field()
    create_prompt_template = CreatePromptTemplateMutation.Field()
    update_prompt_template = UpdatePromptTemplateMutation.Field()
    create_test_cases = CreateTestCasesMutation.Field()
    create_evaluation = CreateEvaluationMutation.Field()

    
class Query(graphene.ObjectType):
    experiment_list = graphene.List(ExperimentType)
    prompt_list_by_pagination = graphene.Field(PromptTemplatePaginationType, experimentId=graphene.String(required=True), limit=graphene.Int(required=True), page=graphene.Int(required=True))
    test_cases = graphene.List(TestCaseType, experimentId=graphene.String(required=True))
    get_report = graphene.Field(ReportType, reportId=graphene.String(required=True),limit=graphene.Int(required=True), page=graphene.Int(required=True))

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
            total_count = None
            if page == 1:
                total_count = PromptTemplate.objects.filter(experiment_id=experimentId).count()
            prompts = PromptTemplate.objects.filter(experiment_id=experimentId).order_by('-updated_at')[offset:offset+limit]

            for prompt in prompts:
                latest_evaluation_report = []
                latest_evaluation_report.append(Evaluation.objects.filter(prompt_template_id=prompt.id).order_by("-updated_at").first())
                prompt.latest_evaluation_report = latest_evaluation_report

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
        
    def resolve_get_report(self, info, reportId=graphene.String(required=True), **kwargs):
        try:
            limit = kwargs.get('limit')
            page = kwargs.get('page')
            offset = (page - 1) * limit
            total_count = None
            if page == 1:
                total_count = EvaluationTestCaseRelation.objects.filter(evaluation_id=reportId).count()
            evaluation_report = Evaluation.objects.get(id=reportId)
            evaluation_report.test_case_evaluation_report = EvaluationTestCaseRelation.objects.filter(evaluation_id=reportId).order_by('-updated_at')[offset:offset+limit]
            evaluation_report.total_count = total_count 
            return evaluation_report
        except Exception as e:
            print(e)
            error = GraphQLError(
            message="Something went wrong",
            extensions= {
             "code": "g_s_q_r_4",
             "debug": "Something_went_wrong",
             }
            )
            return error

    
schema = graphene.Schema(query=Query, mutation=Mutations, types=[ExperimentType, PromptTemplatePaginationType, TestCaseType, ReportType])


