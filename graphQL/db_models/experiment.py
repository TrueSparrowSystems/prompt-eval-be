import json
from mongoengine.fields import (
    StringField,
    ListField,
    IntField,
)
from graphQL.db_models.model_base import ModelBase

class Experiment(ModelBase):
    meta = {'collection': 'experiment'}
    name = StringField(required=True)
    description = StringField(max_length=255)
    dynamic_vars = ListField(StringField(max_length=255))
    
    @classmethod
    def update_dynamic_vars(cls, experiment_id, dynamic_vars_dict):

        experiment = cls.objects(id=experiment_id).first()
        if not experiment:
            raise ValueError('Experiment not found')
        existing_vars = experiment.dynamic_vars or [] 
        new_vars = list(dynamic_vars_dict.keys())
        updated_vars = list(set(existing_vars + new_vars))
        experiment.dynamic_vars = updated_vars
        experiment.save()

