import mongoengine
import sys
from decouple import config
from graphQL.db_models.test_case import TestCase

# To Execute: python -m onetimers.delete_testcases <testcaseIDs>

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
    print("Please provide archive_testcase_id values as command line arguments.")
    sys.exit(1)

archive_testcases_ids = sys.argv[1:]

print('archive_testcases_ids:   ', archive_testcases_ids)

testcases = TestCase.objects.filter(id__in=archive_testcases_ids)
print('testcases:   ', testcases)
for testcase in testcases:
    testcase.status = 'DELETED'
    testcase.save()

