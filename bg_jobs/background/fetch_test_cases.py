from graphQL.db_models.prompt_template import PromptTemplate
from graphQL.db_models.test_case import TestCase

class FetchTestCasesByPromptId:
    def __init__(self, params):
        self.params = params

    def perform(self):
        """
        Perform fetch all test cases by prompt id

        @params: params: A dictionary containing the parameters for the test case.

        @return: A dictionary containing the test case.
        """
        try:
            if not self.params.get('prompt_template_id'):
                self.raise_error("invalid params", "m_e_t_d_p_1")

            # We have prompt_template_id  query get prompt object by querying on prompt_template
            prompt = PromptTemplate.objects.get(id=self.params['prompt_template_id'])
            
            # Get experiment_id from prompt object  
            experiment_id = prompt.experiment_id
            if not experiment_id:
                self.raise_error("invalid params", "m_e_t_d_p_2")    
            
            # Query on test_case_collection and get all test cases for this experiment_id
            test_cases = TestCase.objects(experiment_id=experiment_id)
            
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
    
