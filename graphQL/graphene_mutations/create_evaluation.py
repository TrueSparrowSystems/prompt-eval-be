import graphene
from graphQL.db_models.evalutaions import Evaluations
from .mutation_base import MutateBase
from graphQL.lib.helper import CommonValiator
from graphQL.lib.custom_exception import InvalidLengthError
from graphQL.graphene_types.report import ReportType

class EvaluationInput(graphene.InputObjectType):
    prompt_template_id = graphene.String(required=True)
    model = graphene.String(required=True)
    eval = graphene.String(required=True)
    
    
class CreateEvaluationMutation(MutateBase):
    class Arguments:
        evaluation_data = EvaluationInput(required=True)

    report = graphene.Field(ReportType)

    @classmethod
    def self_mutate(cls, root, info, evaluation_data=None):
        
        # Todo:@Shraddha add validations for model and eval
        # Do query by prompt_template_id 
        
        
        report = Evaluations(prompt_template_id=evaluation_data.prompt_template_id, 
                             model=evaluation_data.model,
                             eval=evaluation_data.eval
                             )
        report.save()
        return CreateEvaluationMutation(report=report)