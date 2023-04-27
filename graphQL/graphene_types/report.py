from graphene import relay,String,Int, List, ObjectType, ID, Float, InputObjectType
from graphQL.graphene_types.evaluation_test_case_relation import EvaluationTestCaseRelationType

class ReportBaseType(ObjectType):
    id = ID()
    model = String()
    eval = String()
    accuracy = Float()
    prompt_template_id = ID()
    run_id = Int()
    status = String()
    initiated_at = Int()
    completed_at = Int()
    created_at = Int()
    updated_at = Int()

class ReportType(ReportBaseType):
    total_count = Int()
    test_case_evaluation_report = List(EvaluationTestCaseRelationType)
