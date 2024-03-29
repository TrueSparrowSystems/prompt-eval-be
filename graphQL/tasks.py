from celery import Task
from api.celery import app
from graphQL.db_models.evaluation_test_case_relation import EvaluationTestCaseRelation
from bg_jobs.run_eval.fetch_test_cases import FetchTestCasesByPromptId

"""
Background job class that performs a series of tasks.

@class BgJob
"""
class BgJob(Task):


    """
    Initializes the BgJob object with the given parameters.

    @params {Object} params
    @params {String} params.evaluation_result_id
    @params {String} params.prompt_template_id
    """
    def __init__(self, params):
        self.params = params

    """
    Performs the background job by executing a series of tasks.
    """
    def perform(self):
        self.params_validation()

        self.fetch_testcases_by_prompt_template_id()

        self.create_evaluation_test_case_relation()



    """
    Validates the parameters to ensure they are valid for further processing.
    """
    def params_validation(self) :
        if (not self.params.get('evaluation_result_id') and
            not self.params.get('prompt_template_id')
            ):
            self.raise_error("invalid params", "p_v_1")

    """
    Fetches test cases based on the prompt template ID.

    @sets self.test_cases

    """
    def fetch_testcases_by_prompt_template_id(self):
        self.test_cases = FetchTestCasesByPromptId(self.params).perform()
        if self.test_cases.count() == 0:
            self.raise_error("no test cases record found", "f_t_c_b_p_t_i_1")


    """
    Creates a relation between evaluation results and test cases.
    """
    def create_evaluation_test_case_relation(self):
        insertObjects = []
        for testcase in self.test_cases:
            # Todo: make a prompt
            insertObjects.append({
                "evaluation_result_id": self.params['evaluation_result_id'],
                "test_case_id": str(testcase.id),
                "test_case_name": testcase.name,
                "test_case_description": testcase.description,
                "acceptable_result": testcase.expected_result
            })

        print("insertObjects length:   ", len(insertObjects), insertObjects[0])
        EvaluationTestCaseRelation.bulk_create_evaluation_test_case_relation(insertObjects)

    """
    Raises an exception with the specified error details.

    @param {String} message
    @param {String} code
    @param {String} debug

    @throws Exception
    """
    def raise_error(self, message, code="bg_p_1", debug="SOMETHING_WENT_WRONG", ):
        error_data = {
            'message': message,
            'debug': debug,
            'code':code
        }

        raise Exception(error_data)




# Register BgJob class with Celery
"""
Executes a background task using the BgJob class.

@params {Object} params
@params {String} params.evaluation_result_id
@params {String} params.prompt_template_id
"""
@app.task
def backgroundTask(params):
    try:
        task = BgJob(params)
        return task.perform()
    except Exception as e:
        print("error while executing BG job------", e)
        return e