from graphene import String, Int, List, ObjectType, ID, JSONString


class TestCaseType(ObjectType):
    id = ID()
    name = String()
    description = String()
    dynamic_var_values = JSONString()
    experiment_id = ID()
    expected_result= List(String)
    created_at = Int()
    updated_at = Int()
