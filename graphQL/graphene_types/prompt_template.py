from graphene import String, Int, List, ObjectType, ID, InputObjectType, Boolean
from graphQL.graphene_types.report import ReportBaseType
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
    is_runnable = Boolean()
    prompts = List(PromptTemplateType)