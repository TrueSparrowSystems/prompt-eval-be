import graphene
from graphQL.db_models.prompt_template import PromptTemplate
from graphQL.db_models.experiment import Experiment
from graphQL.graphene_types.prompt_template import PromptTemplateType, InputConversationType
from .mutation_base import MutateBase
from graphQL.lib.helper import CommonValidator
from graphQL.lib.custom_exception import InvalidLengthError

class UpdatePromptTemplateInput(graphene.InputObjectType):
    id = graphene.String(required=True)
    name = graphene.String()
    description = graphene.String()
    conversation = graphene.List(InputConversationType)


class UpdatePromptTemplateMutation(MutateBase):
    class Arguments:
        update_prompt_template_data = UpdatePromptTemplateInput(required=True)

    prompt_template = graphene.Field(PromptTemplateType)

    """
    update prompt template

    @params {Object} update_prompt_template_data
    @params {String} update_prompt_template_data.id
    @params {String} update_prompt_template_data.name
    @params {String} update_prompt_template_data.description
    @params {String} update_prompt_template_data.conversation

    @returns {Object} UpdatePromptTemplateMutation object
    """
    @classmethod
    def self_mutate(cls, root, info, update_prompt_template_data=None):
        prompt_template = PromptTemplate.objects.get(id=update_prompt_template_data.id)

        if update_prompt_template_data.name:
            if not CommonValidator.max_length_validation(update_prompt_template_data.name, 70):
                raise InvalidLengthError(code = "g_gm_upt_1", param="name")
            prompt_template.name = update_prompt_template_data.name

        if update_prompt_template_data.description:
            if not CommonValidator.max_length_validation(update_prompt_template_data.description, 240):
                raise InvalidLengthError(code = "g_gm_upt_2", param="description")
            prompt_template.description = update_prompt_template_data.description


        if update_prompt_template_data.conversation:
            prompt_template.conversation = update_prompt_template_data.conversation
            Experiment.update_dynamic_vars(prompt_template.experiment_id,update_prompt_template_data.conversation)
        prompt_template.save()
        return UpdatePromptTemplateMutation(prompt_template=prompt_template)