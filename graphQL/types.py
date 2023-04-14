from graphene import relay,String,Int, List, ObjectType, ID, Float, InputObjectType
from graphene_mongo import MongoengineObjectType
from .models import Experiment, Example, PromptTemplate



class ExperimentType(ObjectType):

    id = ID()
    name = String()
    description = String()
    dynamic_vars = List(String)
    created_at = Int()
    updated_at = Int()

class ExperimentPaginationType(ObjectType):
    total_count = Int()
    items = List(ExperimentType)

class ExampleType(MongoengineObjectType):
    class Meta:
        model = Example
        interfaces = (relay.Node,)

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

class InputConversationType(InputObjectType):
    role = String()
    content = String()

class OutputConversationType(ObjectType):
    role = String()
    content = String()

class PromptTemplateType(ObjectType):
    id = ID()
    name = String(required=True)
    description = String()
    conversation = List(OutputConversationType)
    experiment_id = ID(required=True)
    created_at = Int()
    updated_at = Int()