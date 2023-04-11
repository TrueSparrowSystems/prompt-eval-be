from graphene import relay
from graphene_mongo import MongoengineObjectType
from .models import Experiment, Example

class ExperimentType(MongoengineObjectType):
    class Meta:
        model = Experiment
        interfaces = (relay.Node,)

class ExampleType(MongoengineObjectType):
    class Meta:
        model = Example
        interfaces = (relay.Node,)

class ExperimentConnection(relay.Connection):
     class Meta:
        node = ExperimentType



