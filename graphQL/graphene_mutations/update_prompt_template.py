import graphene
from graphQL.graphene_types.prompt_template import PromptTemplateType
from graphQL.db_models.prompt_template import PromptTemplate
from .mutation_base import MutateBase


class UpdatePromptTemplateMutation(MutateBase):
    class Arguments:
        documentId = graphene.String(required=True)
        description = graphene.String()

    promptTemplate = graphene.Field(PromptTemplateType)

    @staticmethod
    def self_mutate(root, info, documentId, description):
        print(documentId)
        query = promptTemplate = PromptTemplate.objects.get(_id=documentId)
        print('Mongoengine queries 1')
        print(str(query.to_mongo()))
        promptTemplate.description = description
        query = promptTemplate.save()
        print('Mongoengine queries 2')
        print(str(query.to_mongo()))
        return UpdatePromptTemplateMutation(promptTemplate=promptTemplate)