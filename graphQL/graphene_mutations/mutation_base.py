import graphene
from django.core.exceptions import ObjectDoesNotExist
from graphQL.lib.custom_exception import CustomException,ParamValidationError
from graphql import GraphQLError
from graphQL.lib.constants.error_codes import INVALID_LENGTH_ERROR

class MutateBase(graphene.Mutation):

    @classmethod
    def self_mutate(cls, root, info, **kwargs):
        raise NotImplementedError('self_mutate must be implemented to use MutateBase')
    
    """
    GraphQL has a built-in error handling mechanism.
    If an exception is raised while resolving a field, the error is captured and returned to the client.
    However, if you want to handle errors in a custom way, you can do so by catching the exception in the resolve method.
    """
    @classmethod
    def mutate(cls,root, info, **kwargs):
        try:
            return cls.self_mutate(root, info, **kwargs)
        except CustomException as e:
            return e
        except ParamValidationError as e:
            return e
        except Exception as e:
            print(e)
            error = GraphQLError(
            message="Something went wrong",
            extensions= {
             "code": "m_b_1",
             "debug": "Something went wrong",
             }
            )
            return error