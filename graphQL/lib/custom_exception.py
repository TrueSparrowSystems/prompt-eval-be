from graphQL.lib.constants.error_codes import INVALID_LENGTH_ERROR
from graphql import GraphQLError


class CustomExpetion(GraphQLError):
    def __init__(self, message, debug="SOMETHING_WENT_WRONG", code="g_l_ce_1"):
        """
        custom exception extend graphene error class

        @return: A dictionary containing the error message, debug message and error code.
        """
        super().__init__(message)
        self.extensions = {
            "code": code,
            "debug": debug,
        }

class ParamValidationError(GraphQLError):
    def __init__(self, message, paramName, debug="INVALID_PARAMETER", code="g_l_ce_2"):
        """
        param validation error extend graphene error class

        @return: A dictionary containing the error message, debug message and error code.
        """
        super().__init__(message)
        self.extensions = {
            "code": code,
            "debug": debug,
            "paramName": paramName
        }

# TODO - Review - Why do we have INVALID_LENGTH_ERROR here and code above
class InvalidLengthError(ParamValidationError):
    """
    Invalid length error extend param validation error class

    @params: param: A string containing the parameter name.
    """
    def __init__(self, code, param, message="Invalid length", debug=INVALID_LENGTH_ERROR):
        super().__init__(message, param, debug, code)
