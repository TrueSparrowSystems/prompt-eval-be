from graphene import relay,String,Int, List, ObjectType, ID, Float, InputObjectType
from graphene_mongo import MongoengineObjectType

class ReportType(ObjectType):
    id = ID()
    model = String(required=True)
    eval = String(required=True)
    accuracy = Float()
    prompt_template_id = ID(required=True)
    evaluation_report_data = String()
    run_id = Int()
    status = String()
    completed_at = Int()
    created_at = Int()
    updated_at = Int()