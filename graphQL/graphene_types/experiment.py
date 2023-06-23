from graphene import String, Int, List, ObjectType, ID

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