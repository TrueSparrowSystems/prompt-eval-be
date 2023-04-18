import graphene
from django.core.exceptions import ObjectDoesNotExist
from graphQL.lib.custom_exception import CustomExpetion,ParamValidationError
from graphql import GraphQLError
from graphQL.lib.constants.error_codes import INVALID_LENGTH_ERROR

class MutateBase(graphene.Mutation):

    @classmethod
    def self_mutate(cls, root, info, **kwargs):
        raise NotImplementedError('self_mutate must be implemented to use MutateBase')
    
    @classmethod
    def mutate(cls,root, info, **kwargs):
        try:
            return cls.self_mutate(root, info, **kwargs)
        except CustomExpetion as e:
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