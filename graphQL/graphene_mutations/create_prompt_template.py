import graphene
from graphQL.graphene_types.prompt_template import PromptTemplateType, InputConversationType
from graphQL.db_models.prompt_template import PromptTemplate
from .mutation_base import MutateBase
    
class CreatePromptTemplateMutation(MutateBase):
    class Arguments:
        name = graphene.String(required=True)
        description = graphene.String()
        conversation = graphene.List(InputConversationType)
        experimentId = graphene.ID(required=True)

    promptTemplate = graphene.Field(PromptTemplateType)

    @staticmethod
    def self_mutate(root, info, name, experimentId, **kwargs):

        promptTemplate = PromptTemplate(name=name, experiment_id=experimentId)
        if 'description' in kwargs:
            promptTemplate.description = kwargs['description']
        if 'conversation' in kwargs:
            promptTemplate.conversation = kwargs['conversation']
        
        promptTemplate.save()
        return CreatePromptTemplateMutation(promptTemplate=promptTemplate)