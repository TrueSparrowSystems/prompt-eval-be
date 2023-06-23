from graphene import ObjectType, String, List, Float, ID


# Define custom conversation type
class OutputConversationType(ObjectType):
    role = String()
    content = String()

# Define custom evaluation test case relation type
class EvaluationTestCaseRelationType(ObjectType):
    id = ID()
    evaluation_id = ID()
    prompt = List(OutputConversationType)
    test_case_id = ID()
    test_case_name = String()
    test_case_description = String()
    actual_result = List(String)
    acceptable_result = List(String)
    accuracy = Float(default_value=None)