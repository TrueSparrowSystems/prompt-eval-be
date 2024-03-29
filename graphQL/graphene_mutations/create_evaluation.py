import graphene
from graphQL.db_models.evaluation import Evaluation
from .mutation_base import MutateBase
from graphQL.graphene_types.report import ReportBaseType

from bg_jobs.background_job import background_job
from bg_jobs.executor import SingletonThreadPoolExecutor


class EvaluationInput(graphene.InputObjectType):
    prompt_template_id = graphene.String(required=True)
    model = graphene.String(required=True)
    eval = graphene.String(required=True)


class CreateEvaluationMutation(MutateBase):
    class Arguments:
        evaluation_data = EvaluationInput(required=True)

    report = graphene.Field(ReportBaseType)

    """
    create evaluation report

    @params {Object} evaluation_data
    @params {String} evaluation_data.prompt_template_id
    @params {String} evaluation_data.model
    @params {String} evaluation_data.eval

    @returns {Object} CreateEvaluationMutation object
    """
    @classmethod
    def self_mutate(cls, root, info, evaluation_data=None):
        report = Evaluation(prompt_template_id=evaluation_data.prompt_template_id, 
                             model=evaluation_data.model,
                             eval=evaluation_data.eval
                             )
        report.save()
        bg_params = {
            "evaluation_id": str(report.id),
            "prompt_template_id": str(report.prompt_template_id)
        }
        
        executor = SingletonThreadPoolExecutor()
        executor.submit(background_job, bg_params)

        return CreateEvaluationMutation(report=report)