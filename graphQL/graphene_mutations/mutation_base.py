import graphene
from django.core.exceptions import ObjectDoesNotExist
from graphql import GraphQLError

class MutateBase(graphene.Mutation):

    @staticmethod
    def self_mutate(root, info, **kwargs):
        raise NotImplementedError('self_mutate must be implemented to use MutateBase')
    
    @classmethod
    def mutate(cls,root, info, **kwargs):
        try:
            return cls.self_mutate(root, info, **kwargs)
        except Exception as e:
            print(e)
            error = GraphQLError(
            message="Something went wrong",
            extensions= {
             "code": "m_b_1",
             "debug": "Something_went_wrong",
             }
            )
            return error