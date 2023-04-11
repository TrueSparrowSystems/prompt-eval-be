from graphene import relay
from graphene_mongo import MongoengineObjectType
from .models import Experiment


class ExperimentType(MongoengineObjectType):
    class Meta:
        model = Experiment
        interfaces = (relay.Node,)
