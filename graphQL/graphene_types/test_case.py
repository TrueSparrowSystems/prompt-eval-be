from graphene import relay,String,Int, List, ObjectType, ID, Float, InputObjectType, JSONString


class TestCaseType(ObjectType):
    id = ID()
    name = String()
    description = String()
    dynamic_var_values = JSONString()
    experiment_id = ID()
    expected_result= List(String)
    created_at = Int()
    updated_at = Int()
