from graphene import relay,String,Int, List, ObjectType, ID, Float, InputObjectType, JSONString


class GetEvalAndModelType(ObjectType):
    models = List(String)
    evals = List(String)


