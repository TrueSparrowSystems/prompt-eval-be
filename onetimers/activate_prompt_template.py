import mongoengine
import sys
from decouple import config
from graphQL.db_models.prompt_template import PromptTemplate

_MONGODB_USER = config('PE_MONGODB_USER')
_MONGODB_PASSWD = config('PE_MONGODB_PASSWORD')
_MONGODB_HOST = config('PE_MONGODB_HOST')
_MONGODB_NAME = config('PE_MONGODB_NAME')
_MONGODB_PORT = int(config('PE_MONGODB_PORT'))

mongoengine.connect(
    _MONGODB_NAME,
    username=_MONGODB_USER,
    password=_MONGODB_PASSWD,
    host=_MONGODB_HOST,
    port=_MONGODB_PORT
)

if len(sys.argv) < 2:
    print("Please provide archive_prompt_templates_ids values as command line arguments.")
    sys.exit(1)

archive_prompt_templates_ids = sys.argv[1:]

print('archive_prompt_templates_ids:   ', archive_prompt_templates_ids)

promptTemplates = PromptTemplate.objects.filter(id__in=archive_prompt_templates_ids)
print('promptTemplatess:   ', promptTemplates)
for promptTemplate in promptTemplates:
    promptTemplate.status = 'ACTIVE'
    promptTemplate.save()





