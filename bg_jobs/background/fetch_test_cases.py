from graphQL.db_models.prompt_template import PromptTemplate
from graphQL.db_models.test_case import TestCase, Status as TestCaseStatus


"""
fetch all test cases by prompt id

@class FetchTestCasesByPromptId
"""
class FetchTestCasesByPromptId:
    """
    initialize params

    @params {Object} params
    @params {String} params.prompt_template_id

    @returns {Object} params
    """
    def __init__(self, params):
        self.params = params

    """
    Perform fetch all test cases by prompt id

    @returns {Object} test_cases
    """
    def perform(self):
        try:
            if not self.params.get('prompt_template_id'):
                self.raise_error("invalid params", "m_e_t_d_p_1")

            prompt = PromptTemplate.objects.get(id=self.params['prompt_template_id'])
            
            experiment_id = prompt.experiment_id
            if not experiment_id:
                self.raise_error("invalid params", "m_e_t_d_p_2")    
            
            test_cases = TestCase.objects(experiment_id=experiment_id, status=TestCaseStatus.ACTIVE)
            
            return test_cases
        except Exception as e:
            return(e)
            
    def raise_error(self, message, code= "m_e_t_c_r_d",debug="SOMETHING_WENT_WRONG" ):
        error_data = {
            "message": message,
            "debug": debug,
            "code":code
        }
                
        raise Exception(error_data)
    
