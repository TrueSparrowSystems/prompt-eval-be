from graphene import ObjectType, String, Int, List, Field, Float, ID

class EvaluationTestCaseRelationType(ObjectType):
    id = ID()
    evaluation_id = ID()
    prompt = String()
    test_case_id = ID()
    test_case_name = String()
    test_case_description = String()
    actual_result = List(String)
    acceptable_result = List(String)
    accuracy = Float()