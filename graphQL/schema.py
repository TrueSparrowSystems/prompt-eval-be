import graphene
from graphene.relay import Node
from graphene_mongo.fields import MongoengineConnectionField
from .mutations import CreateExperimentMutation
from .models import Experiment
from .types import ExperimentType


class Mutations(graphene.ObjectType):
    create_experiment = CreateExperimentMutation.Field()

class Query(graphene.ObjectType):
    node = Node.Field()
    experiment_list = graphene.List(ExperimentType)

    def resolve_experiment_list(root, info):
        return Experiment.objects.all()

schema = graphene.Schema(query=Query, mutation=Mutations, types=[ExperimentType])
