from graphene import relay,String,Int, List, ObjectType, ID, Float, InputObjectType

class OutputDynamicVarType(ObjectType):
    key = String()
    value = String()

class InputDynamicVarType(InputObjectType):
    key = String()
    value = String()

class TestCaseType(ObjectType):
    id = ID()
    name = String()
    description = String()
    dynamic_var_values = List(OutputDynamicVarType)
    experiment_id = ID()
    expected_result= List(String)
    created_at = Int()
    updated_at = Int()
