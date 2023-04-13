from graphene import relay,String,Int, List, ObjectType
from graphene_mongo import MongoengineObjectType
from .models import Experiment, Example, PromptTemplate

class DynamicVarsType(ObjectType):
    key = String(required=True)
    value = String(required=True)

class ExperimentType(MongoengineObjectType):
    class Meta:
        model = Experiment
    
    name = String(required=True)
    description = String(required=True)
    dyanamic_vars = List(DynamicVarsType)
    created_at = Int()
    updated_at = Int()

class ExperimentPaginationType(ObjectType):
    total_count = Int()
    items = List(ExperimentType)

class ExampleType(MongoengineObjectType):
    class Meta:
        model = Example
        interfaces = (relay.Node,)



class PromptTemplateType(MongoengineObjectType):
    
    class Meta:
        model = PromptTemplate
        interfaces = (relay.Node,)