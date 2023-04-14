from graphene import relay,String,Int, List, ObjectType, ID, Float, InputObjectType
from graphene_mongo import MongoengineObjectType

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