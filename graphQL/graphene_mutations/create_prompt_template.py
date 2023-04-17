import graphene
from graphQL.graphene_types.prompt_template import PromptTemplateType, InputConversationType
from graphQL.db_models.prompt_template import PromptTemplate
from .mutation_base import MutateBase
from graphQL.lib.helper import CommonValiator
    
class CreatePromptTemplateMutation(MutateBase):
    class Arguments:
        name = graphene.String(required=True)
        description = graphene.String()
        conversation = graphene.List(InputConversationType)
        experimentId = graphene.ID(required=True)

    promptTemplate = graphene.Field(PromptTemplateType)

    @staticmethod
    def self_mutate(root, info, name, experimentId, **kwargs):
        if not CommonValiator.length_validation(name, 70):
            raise Exception('Invalid name length')

        promptTemplate = PromptTemplate(name=name, experiment_id=experimentId)
        if 'description' in kwargs:
            if not CommonValiator.length_validation(kwargs['description'], 240):
                raise Exception('Invalid description length')
            promptTemplate.description = kwargs['description']
        if 'conversation' in kwargs:
            promptTemplate.conversation = kwargs['conversation']
        
        promptTemplate.save()
        return CreatePromptTemplateMutation(promptTemplate=promptTemplate)