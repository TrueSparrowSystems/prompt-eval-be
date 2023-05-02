from graphQL.db_models.evaluation_test_case_relation import EvaluationTestCaseRelation
from graphQL.db_models.evaluation import Evaluation
from graphQL.db_models.prompt_template import PromptTemplate
from .fetch_test_cases import FetchTestCasesByPromptId
from .create_prompt import CreatePrompt
from decouple import config
import json, time


class BgJob():
    def __init__(self, params):
        self.params = params

    def perform(self):
        try:
            self.params_validation()
            
            self.update_evaluation_status()
            
            self.fetch_testcases_by_prompt_template_id()
            
            self.create_evaluation_test_case_relation()
            
            self.create_jsonl_file()
            
            self.create_yaml_file()
            
            self.run_evaluation()
            
            self.update_evaluation_test_case_relation()
            
            self.update_evaluation()
        except Exception as e:
            print(e)
            self.update_evaluation_on_error()
        
    def params_validation(self) :
        if (not self.params.get('evaluation_id') and 
            not self.params.get('prompt_template_id')  
            ):
            self.raise_error("invalid params", "bg_j_b_bg_j_p_v_1")
            
    def update_evaluation_status(self):
        self.evaluation = Evaluation.objects.get(id=self.params['evaluation_id'])
        self.evaluation.status = 'RUNNING'
        self.evaluation.save()
            
    def fetch_testcases_by_prompt_template_id(self):
        self.test_cases = FetchTestCasesByPromptId(self.params).perform()
        if self.test_cases.count() == 0:
            self.raise_error("no test cases record found", "f_t_c_b_p_t_i_1")
    
        
    def create_evaluation_test_case_relation(self):
        
        self.prompt_template_obj = PromptTemplate.prompt_by_id(self.params['prompt_template_id'])
        insertObjects = []
        jsonl_order = 1
        for testcase in self.test_cases:
            prompt = self.create_prompt(testcase)
            insertObjects.append({
                "evaluation_id": self.params['evaluation_id'],
                "prompt": prompt,
                "test_case_id": str(testcase.id),
                "test_case_name": testcase.name,
                "test_case_description": testcase.description,
                "acceptable_result": testcase.expected_result,
                "jsonl_order": jsonl_order
            })
            jsonl_order += 1
        
        print("insertObjects length:   ", len(insertObjects), insertObjects[0])
        EvaluationTestCaseRelation.bulk_create_evaluation_test_case_relation(insertObjects)  
        
    def create_prompt(self, testcase):
        
        prompt = CreatePrompt({
            'test_case': testcase, 
            'prompt_template_obj': self.prompt_template_obj
            }).perform()
        
        print('prompt-----------', prompt)
        
        return prompt    
    
    def create_jsonl_file(self):
        
        evaluation_test_case_relation_records = EvaluationTestCaseRelation.objects.filter(
            evaluation_id=self.params['evaluation_id']
        ).order_by('jsonl_order')
        
        print('evaluation_test_case_relation_records:   ', evaluation_test_case_relation_records.count())
        
        jsonl_base_path = config('PE_JSONL_FOLDER_BASE_PATH')
        unix_time = int(time.time())
        jsonl_file = jsonl_base_path + str(self.params['evaluation_id']) + '_' + unix_time + '.jsonl'
        print('jsonl_file:   ', jsonl_file)
        with open(jsonl_file, mode='w') as output_jsonl:
            for evaluation_test_case_relation_record in evaluation_test_case_relation_records:
                prompt = evaluation_test_case_relation_record['prompt']
                acceptable_result = evaluation_test_case_relation_record['acceptable_result']
                data = {'input': prompt, 'ideal': acceptable_result}
                print('data:   ', data)
                json.dump(data, output_jsonl)
                output_jsonl.write('\n')
 
    def create_yaml_file(self):
        
        yaml_base_path = config('PE_YAML_FOLDER_BASE_PATH')
        unix_time = int(time.time())
        yaml_path = yaml_base_path + str(self.params['evaluation_id']) + '_' + unix_time + '.yaml'
        print('yaml_path:   ', yaml_path)        
        pass  
    
    def run_evaluation(self):
        pass
    
    def update_evaluation_test_case_relation(self):
        pass
    
    def update_evaluation(self):
        pass
    
    def update_evaluation_on_error(self):
        pass
       
    def raise_error(self, message, code="bg_p_1", debug="SOMETHING_WENT_WRONG", ):
        error_data = {
            'message': message,
            'debug': debug,
            'code':code
        }
        
        raise Exception(error_data)
        
           


