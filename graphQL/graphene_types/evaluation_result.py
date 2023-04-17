from graphene import relay,String,Int, List, ObjectType, ID, Float, InputObjectType
from graphQL.graphene_types.test_case_evaluation_result import TestCasesEvaluationsResult

class ReportType(ObjectType):
    id = ID()
    model = String()
    eval = String()
    accuracy = Float()
    prompt_template_id = ID()
    evaluation_report_data = String()
    run_id = Int()
    status = String()
    completed_at = Int()
    created_at = Int()
    updated_at = Int()
    evaluation_report_data = List(TestCasesEvaluationsResult)