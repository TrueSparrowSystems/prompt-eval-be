from graphene import String, List, ObjectType


class GetEvalAndModelType(ObjectType):
    models = List(String)
    evals = List(String)


