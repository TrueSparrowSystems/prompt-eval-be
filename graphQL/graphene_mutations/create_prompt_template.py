import graphene
from graphQL.graphene_types.prompt_template import PromptTemplateType, InputConversationType
from graphQL.db_models.prompt_template import PromptTemplate

    
class CreatePromptTemplateMutation(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        description = graphene.String()
        conversation = graphene.List(InputConversationType)
        experimentId = graphene.ID(required=True)

    promptTemplate = graphene.Field(PromptTemplateType)

    def mutate(root, info, name,experimentId, **kwargs):

        fields = {}
        for arg_name, arg_value in kwargs.items():
            if arg_name in ['description', 'conversation']:
                fields[arg_name] = arg_value
        
        promptTemplate = PromptTemplate(name=name, experiment_id=experimentId, **fields)
        promptTemplate.save()
        return CreatePromptTemplateMutation(promptTemplate=promptTemplate)