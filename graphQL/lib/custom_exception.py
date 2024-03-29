from graphQL.lib.constants.error_codes import INVALID_LENGTH_ERROR, INVALID_STATUS, OBJECT_NOT_FOUND
from graphql import GraphQLError

"""
custom exception class for defining custom exceptions

@class CustomExpetion
"""
class CustomException(GraphQLError):
    """
    custom exception extend graphene error class

    @params {String} message
    @params {String} debug
    @params {String} code
    """
    def __init__(self, message, debug="SOMETHING_WENT_WRONG", code="g_l_ce_1"):
        super().__init__(message)
        self.extensions = {
            "code": code,
            "debug": debug,
        }

"""
param validation error class for defining param validation errors

@class ParamValidationError
"""
class ParamValidationError(GraphQLError):
    """
    param validation error extend graphene error class

    @params {String} message
    @params {String} paramName
    @params {String} debug
    @params {String} code
    """
    def __init__(self, message, paramName, debug="INVALID_PARAMETER", code="g_l_ce_2"):
        super().__init__(message)
        self.extensions = {
            "code": code,
            "debug": debug,
            "paramName": paramName
        }

"""
invalid length error class for defining invalid length errors

@class InvalidLengthError
"""
class InvalidLengthError(ParamValidationError):
    """
    Invalid length error extend param validation error class

    @params {String} message
    @params {String} paramName
    @params {String} debug
    @params {String} code
    """
    def __init__(self, code, param, message="Invalid length", debug=INVALID_LENGTH_ERROR):
        super().__init__(message, param, debug, code)

"""
Invalid status check

@class InvalidStatus
"""
class InvalidStatusError(ParamValidationError):
    """
    Invalid length error extend param validation error class

    @params {String} message
    @params {String} paramName
    @params {String} debug
    @params {String} code
    """
    def __init__(self, code, param, message="Invalid status", debug=INVALID_STATUS):
        super().__init__(message, param, debug, code)

"""
@class Invalid id
"""
class ObjectNotFoundError(ParamValidationError):
    """
    Object not found extends param validation error class

    @params {String} message
    @params {String} paramName
    @params {String} debug
    @params {String} code
    """
    def __init__(self, code, param, message="Object not found", debug=OBJECT_NOT_FOUND):
        super().__init__(message, param, debug, code)


