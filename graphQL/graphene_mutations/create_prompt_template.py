import graphene
from graphQL.graphene_types.prompt_template import PromptTemplateType, InputConversationType
from graphQL.db_models.prompt_template import PromptTemplate
from graphQL.db_models.experiment import Experiment
from .mutation_base import MutateBase
from graphQL.lib.helper import CommonValiator
from graphQL.lib.custom_exception import InvalidLengthError

class PromptTemplateInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    description = graphene.String()
    conversation = graphene.List(InputConversationType)
    experiment_id = graphene.ID(required=True)
    
class CreatePromptTemplateMutation(MutateBase):
    class Arguments:
        prompt_template_data = PromptTemplateInput(required=True)

    promptTemplate = graphene.Field(PromptTemplateType)

    """
    create prompt template

    @params {Object} prompt_template_data
    @params {String} prompt_template_data.name
    @params {String} prompt_template_data.description
    @params {String} prompt_template_data.conversation
    @params {String} prompt_template_data.experiment_id

    @returns {Object} CreatePromptTemplateMutation object
    """
    @classmethod
    def self_mutate(cls, root, info, prompt_template_data=None):
        if not CommonValiator.max_length_validation(prompt_template_data.name, 70):
            raise InvalidLengthError(code = "g_gm_cpt_1", param="name")

        promptTemplate = PromptTemplate(name=prompt_template_data.name, experiment_id=prompt_template_data.experiment_id)
        if prompt_template_data.description:
            if not CommonValiator.max_length_validation(prompt_template_data.description, 240):
                raise InvalidLengthError(code = "g_gm_cpt_1", param="description")
            promptTemplate.description = prompt_template_data.description
        if prompt_template_data.conversation:
            promptTemplate.conversation = prompt_template_data.conversation
            Experiment.update_dynamic_vars(prompt_template_data.experiment_id,prompt_template_data.conversation)
        promptTemplate.status = 'ACTIVE'
        promptTemplate.save()
        return CreatePromptTemplateMutation(promptTemplate=promptTemplate)