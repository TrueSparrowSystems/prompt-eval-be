from graphQL.lib.constants.error_codes import INVALID_LENGTH_ERROR
from graphql import GraphQLError


class CustomExpetion(GraphQLError):
    def __init__(self, message, debug="SOMETHING_WENT_WRONG", code="g_l_ce_1"):
        super().__init__(message)
        self.extensions = {
            "code": code,
            "debug": debug,
        }

class ParamValidationError(GraphQLError):
    def __init__(self, message, paramName, debug="INVALID_PARAMETER", code="g_l_ce_2"):
        super().__init__(message)
        self.extensions = {
            "code": code,
            "debug": debug,
            "paramName": paramName
        }

class InvalidLengthError(ParamValidationError):
    def __init__(self, code, param, message="Invalid length", debug=INVALID_LENGTH_ERROR):
        super().__init__(message, param, debug, code)
