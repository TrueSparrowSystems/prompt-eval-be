from graphQL.db_models.evaluation_test_case_relation import EvaluationTestCaseRelation
from graphQL.db_models.evaluation import Evaluation
from graphQL.db_models.prompt_template import PromptTemplate
from .fetch_test_cases import FetchTestCasesByPromptId
from .create_prompt import CreatePrompt
from decouple import config
import json, time
import yaml
from evals_framework.evals.cli import oaieval

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
            
            self.update_evals_parameter()
            
            self.run_evaluation()
            
            self.update_evaluation_test_case_relation()
            
            self.update_evaluation()
        except Exception as e:
            print(str(e))
            self.update_evaluation_on_error(e)
            # Todo:  call perform with condition retry_count < 0 and status = failed
            
        
    def params_validation(self) :
        if (not self.params.get('evaluation_id') and 
            not self.params.get('prompt_template_id')  
            ):
            self.raise_error("invalid params", "bg_j_b_bg_j_p_v_1")
            
    def update_evaluation_status(self):
        self.evaluation = Evaluation.objects.get(id=self.params['evaluation_id'])
        if (self.evaluation.status != 'INITIATED'):
            self.evaluation.initiated_at  = int(time())
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
        base_dir = config('PE_DIRECTORY_BASE_PATH')
        unix_time = int(time.time())
        self.jsonl_file = base_dir + jsonl_base_path + str(self.params['evaluation_id']) + '_' + unix_time + '.jsonl'
        print('jsonl_file:   ', self.jsonl_file)
        with open(self.jsonl_file, mode='w') as output_jsonl:
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
        base_dir = config('PE_DIRECTORY_BASE_PATH')
        # Todo:: create folder with timestamp inside yaml folder
        self.yaml_file = base_dir + yaml_base_path + str(self.params['evaluation_id']) + '_' + unix_time + '.yaml'
        print('yaml_file:   ', self.yaml_file)        
        base_yaml_file = base_dir + 'YAML/base.yaml'
        
        print('base_yaml_file:   ', base_yaml_file)
        
        # for now eval_name, evaluation_id, version, class_name, jsonl_file_path, 
        # fuzzy, extract_gql are hardcoded
        eval_name = self.evaluation['eval']
        evaluation_id = self.params['evaluation_id']
        version = 'V0'
        # Todo:: read from globals
        class_name = 'classname'
        jsonl_file_path = self.jsonl_file
        # Todo: do conditional on eval_name
        fuzzy = False
        extract_gql = False
        
        with open(base_yaml_file, "r") as file:
            # Load the YAML contents into a Python dictionary
            yaml_dict = yaml.safe_load(file)
            yaml_str = yaml.dump(yaml_dict)
            yaml_str = yaml_str.replace("{{eval_name}}", eval_name)
            yaml_str = yaml_str.replace("{{evaluation_id}}", evaluation_id)
            yaml_str = yaml_str.replace("{{version}}", version)
            yaml_str = yaml_str.replace("{{class_name}}", class_name)
            yaml_str = yaml_str.replace("{{jsonl_file_path}}", jsonl_file_path)
            yaml_str = yaml_str.replace("{{fuzzy}}", fuzzy)
            yaml_str = yaml_str.replace("{{extract_gql}}", extract_gql)
            
        # Todo:: check file format
        with open(self.yaml_file, "w") as file:
            # Write the modified YAML contents back to the file
            file.write(yaml_str)


    def update_evals_parameter(self):  
        self.evaluation = Evaluation.objects.get(id=self.params['evaluation_id'])
        self.evaluation.evals_parameter = {
            'jsonl_file_path': self.jsonl_file,
            'yaml_file_path': self.yaml_file
        }
        self.evaluation.save()
                
    def run_evaluation(self):
        #try:
        # args = [  
        #     completion_fn='model_name',
        #     eval='eval_name',
        #     record_path='/path/to/output/file/name.jsonl',
        #     registry_path=['/base/path/to/evals/registry']
        # ]
        
        # #oaieval.run(args)
        #Todo: make output file path in yaml sub folder
        pass
    
    def update_evaluation_test_case_relation(self):
        pass
    
    def update_evaluation(self):
        self.evaluation = Evaluation.objects.get(id=self.params['evaluation_id'])
        self.evaluation.status = 'COMPLETED'
        self.evaluation.accuracy = 20
        self.evaluation.run_id = 20
        self.evaluation.completed_at  = int(time())
        self.evaluation.save()
    
    def update_evaluation_on_error(self, error):
        self.evaluation = Evaluation.objects.get(id=self.params['evaluation_id'])
        self.evaluation.status = 'FAILED'
        self.evaluation.error_object = str(error)
        self.evaluation.initiated_at = 0
        self.evaluation.completed_at = 0
        self.evaluation.retry_count = int(self.evaluation.retry_count) + 1
        self.evaluation.evals_parameter = {}
        self.evaluation.save()
       
    def raise_error(self, message, code="bg_p_1", debug="SOMETHING_WENT_WRONG", ):
        error_data = {
            'message': message,
            'debug': debug,
            'code':code
        }
        
        raise Exception(error_data)
        
           


