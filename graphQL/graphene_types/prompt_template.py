from graphene import relay,String,Int, List, ObjectType, ID, Float, InputObjectType
from graphene_mongo import MongoengineObjectType
from graphQL.graphene_types.report import ReportType, ReportBaseType
class InputConversationType(InputObjectType):
    role = String()
    content = String()

class OutputConversationType(ObjectType):
    role = String()
    content = String()

class PromptTemplateType(ObjectType):
    id = ID()
    name = String()
    description = String()
    conversation = List(OutputConversationType)
    experiment_id = ID()
    latest_evaluation_report = List(ReportBaseType)
    created_at = Int()
    updated_at = Int()

class PromptTemplatePaginationType(ObjectType):
    total_count = Int()
    total_test_cases_count = Int()
    prompts = List(PromptTemplateType)