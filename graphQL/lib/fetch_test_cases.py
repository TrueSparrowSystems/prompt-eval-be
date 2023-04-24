from graphQL.db_models.prompt_template import PromptTemplate
from graphQL.db_models.test_case import TestCase

class FetchTestCasesByPromptId:
    def __init__(self, params):
        self.params = params

    def perform(self):
        try:
            print("FetchTestCasesByPromptId perform method called", self.params)
            if not self.params.get('prompt_template_id'):
                self.raise_error("invalid params", "m_e_t_d_p_1")

            # We have prompt_template_id  query get prompt object by querying on prompt_template
            prompt = PromptTemplate.objects.get(id=self.params['prompt_template_id'])
            print("prompt Id:   ", prompt.id)
            
            # Get experiment_id from prompt object  
            experiment_id = prompt.experiment_id
            if not experiment_id:
                self.raise_error("invalid params", "m_e_t_d_p_2")    
            print("experiment_id:   ", experiment_id)
            
            # Query on test_case_collection and get all test cases for this experiment_id
            test_cases = TestCase.objects(experiment_id=experiment_id)
            print("test_cases length:   ", test_cases.count())
            
            # Todo: make a prompt
            return test_cases
        except Exception as e:
            print(e)
            return(e)
            
        
        
    def raise_error(self, message, code= "m_e_t_c_r_d",debug="SOMETHING_WENT_WRONG" ):
        error_data = {
            "message": message,
            "debug": debug,
            "code":code
        }
                
        raise Exception(error_data)
    
