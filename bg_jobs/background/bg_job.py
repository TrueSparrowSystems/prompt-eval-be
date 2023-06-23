from graphQL.db_models.evaluation_test_case_relation import EvaluationTestCaseRelation
from graphQL.db_models.evaluation import Evaluation, Status
from graphQL.db_models.prompt_template import PromptTemplate
from .fetch_test_cases import FetchTestCasesByPromptId
from .create_prompt import CreatePrompt
from decouple import config
import json, time
import yaml
from evals_framework.evals.cli import oaieval
from bg_jobs.background.eval_arguments import EvalArguments
import  bg_jobs.globals as globals
import subprocess
import os
import shutil

"""
bg job class which perform background job for evaluation

@class BgJob
"""
class BgJob():
    """
    Constructor for the BgJob class.

    @params {Object} params
    @params {String} params.evaluation_id
    @params {String} params.prompt_template_id
    """
    def __init__(self, params):
        self.params = params
        self.accuracy = 0
        self.run_id = 0

    def perform(self):
        try:
            print('****************BGJOB Perform ****************')
            
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
            
            self.clean_up()
            
        except Exception as e:
            self.update_evaluation_on_error(e)
            self.evaluation = Evaluation.objects.get(id=self.params['evaluation_id'])
            
            EvaluationTestCaseRelation.delete_records_by_evaluation_id(evaluation_id=self.params['evaluation_id'])
            self.clean_up()

            if(self.evaluation.retry_count <= 3 and self.evaluation.status == Status['FAILED']):
                print('************* Retrying BGJOB Perform ****************')
                self.perform()
            else:
                print('************** Failed executing BG job after retries ****************')
                return str(e)
            
        
    """
    check if evaluation_id or prompt_template_id is present in params
    """
    def params_validation(self) :
        print('****************BGJOB params_validation ****************')
        if (not self.params.get('evaluation_id') and 
            not self.params.get('prompt_template_id')  
            ):
            self.raise_error("invalid params", "bg_j_b_bg_j_p_v_1")
            
    """
    update status of evaluation to RUNNING and update initiated_at

    @sets {Object} self.evaluation
    """
    def update_evaluation_status(self):
        try:
            print('****************BGJOB update_evaluation_status ****************')
            self.evaluation = Evaluation.objects.get(id=self.params['evaluation_id'])
            if (self.evaluation['status'] != 'INITIATED'):
                self.evaluation.initiated_at  = int(time.time())
            self.evaluation.status = Status['RUNNING']
            self.evaluation.save()
        except Exception as e:
            self.raise_error(f"error while updating status:: {str(e)}", "bg_j_b_u_e_s_1")

            
    """
    fetch testcases by prompt_template_id

    @sets {Object} self.test_cases
    """
    def fetch_testcases_by_prompt_template_id(self):
        try:
            self.test_cases = FetchTestCasesByPromptId(self.params).perform()
            if self.test_cases.count() == 0:
                self.raise_error("no test cases record found", "f_t_c_b_p_t_i_1")
        except Exception as e:
            self.raise_error(f"error while fetching test cases: {str(e)}", "f_t_c_b_p_t_i_2")
    
    """
    create evaluation test case relation make entry in evaluation_test_case_relation table

    @sets {Object} self.evaluation_test_case_relation_records
    """
    def create_evaluation_test_case_relation(self):
        try:
            self.prompt_template_obj = PromptTemplate.prompt_by_id(self.params['prompt_template_id'])
            insertObjects = []
            jsonl_order = 0
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
            
            EvaluationTestCaseRelation.bulk_create_evaluation_test_case_relation(insertObjects)  
        except Exception as e:
            self.raise_error(f"error while creating evaluation test case relation {str(e)}", "c_e_t_c_r_1")
        
    """
    create prompt by replacing dynamic variables with values in prompt template by test case

    @params {Object} testcase
    @params {Object} self.prompt_template_obj

    @returns {Object} prompt
    """
    def create_prompt(self, testcase):
        prompt = CreatePrompt({
            'test_case': testcase, 
            'prompt_template_obj': self.prompt_template_obj
            }).perform()
                
        return prompt    
    
    """
    create input jsonl file for evals framework

    @sets {Object} self.evaluation_test_case_relation_records
    """
    def create_jsonl_file(self):
        try:
            self.evaluation_test_case_relation_records = EvaluationTestCaseRelation.objects.filter(
                evaluation_id=self.params['evaluation_id']
            ).order_by('jsonl_order')
            
            jsonl_base_path = config('PE_JSONL_FOLDER_BASE_PATH')
            jsonl_folder_path = os.path.join(os.getcwd(), jsonl_base_path)
            if not os.path.exists(jsonl_folder_path):
                os.makedirs(jsonl_folder_path)
            unix_time = int(time.time())
            
            self.jsonl_file = os.path.join(jsonl_folder_path, str((self.params['evaluation_id'])) + '_' + str(unix_time) + '.jsonl')

            with open(self.jsonl_file, mode='w') as output_jsonl:
                for evaluation_test_case_relation_record in self.evaluation_test_case_relation_records:
                    prompt = evaluation_test_case_relation_record['prompt']
                    acceptable_result = evaluation_test_case_relation_record['acceptable_result']
                    data = {'input': prompt, 'ideal': acceptable_result}
                
                    json.dump(data, output_jsonl)
                    output_jsonl.write('\n')
        except Exception as e:
            self.raise_error(str(e), "c_j_f_1")
 
    """
    create ymal file for choosing evaluator for evals framework
    build new ymal file from base ymal file according to eval name

    @sets {Object} self.yaml_file
    """
    def create_yaml_file(self):
        try:
            self.yaml_folder = os.path.join(os.getcwd(), config('PE_YAML_FOLDER_BASE_PATH'))
            self.eval_folder = os.path.join(self.yaml_folder, 'evals')
            
            unix_time = int(time.time())
            if not os.path.exists(self.yaml_folder):
                os.mkdir(self.yaml_folder)
                
            if not os.path.exists(self.eval_folder):
                os.mkdir(self.eval_folder)

            self.yaml_file = os.path.join(self.eval_folder, str(self.params['evaluation_id']) + '_' + str(unix_time) + '.yaml')
                
            base_yaml_file = os.path.join(self.yaml_folder, 'base.yaml')
            
            eval_name = self.evaluation['eval']
            evaluation_id = self.params['evaluation_id']
            version = 'v0'
            class_name = globals.EVALS_CLASS_DICT[eval_name]
            jsonl_file_path = self.jsonl_file
            fuzzy_boolean = False
            extract_gql_boolean = False
            if eval_name == 'graphql':
                fuzzy_boolean = True
                extract_gql_boolean = True
            
            with open(base_yaml_file, "r") as file:
                # Load the YAML contents into a Python dictionary
                yaml_dict = yaml.load(file, Loader=yaml.FullLoader)
                if eval_name != 'graphql':
                    del yaml_dict['eval_name.evaluation_id.version']['args']['fuzzy']
                    del yaml_dict['eval_name.evaluation_id.version']['args']['extract_gql']
                yaml_str = yaml.dump(yaml_dict)
                yaml_str = yaml_str.replace("eval_name", eval_name)
                yaml_str = yaml_str.replace("evaluation_id", str(evaluation_id))
                yaml_str = yaml_str.replace("version", version)
                yaml_str = yaml_str.replace("metrics_list", "[accuracy]")
                yaml_str = yaml_str.replace("class_name", class_name)
                yaml_str = yaml_str.replace("jsonl_file_path", jsonl_file_path)
                yaml_str = yaml_str.replace("fuzzy_boolean", str(fuzzy_boolean))
                yaml_str = yaml_str.replace("extract_gql_boolean", str(extract_gql_boolean))

            with open(self.yaml_file, "w") as file:
                file.write(yaml_str)
        except Exception as e:
            self.raise_error(str(e), "c_y_f_1" )


    """
    update evals parameter in evaluation table

    @sets {Object} self.evaluation
    """
    def update_evals_parameter(self):  
        try:
            self.evaluation = Evaluation.objects.get(id=self.params['evaluation_id'])
            self.evaluation.eval_parameter = {
                'jsonl_file_path': self.jsonl_file,
                'yaml_file_path': self.yaml_file
            }
            self.evaluation.save()
        except Exception as e:
            self.raise_error(str(e), "u_e_p_1" )
                
    """
    run evaluation using CLI by making command which take jsoln file and ymal file as input

    @sets {Object} self.evaluation
    """
    def run_evaluation(self):
        try:
            
            completion_fn = self.evaluation['model']
            eval = self.evaluation['eval'] + '.' + str(self.params['evaluation_id'])
            self.record_path = os.path.join(self.eval_folder, f"output_{str(self.params['evaluation_id'])}.jsonl")
            registry_path = self.yaml_folder
            

            command = f"oaieval {completion_fn} {eval} --debug --registry_path {registry_path} --record_path {self.record_path}"
            print('command--------', command)
            with subprocess.Popen(command.split(), stdout=subprocess.PIPE, bufsize=1, universal_newlines=True) as p:
                for line in p.stdout:
                    print(line, end='')

        except Exception as e:
            self.raise_error(str(e), "bg_j_b_bg_j_r_e_1", "EVALS_RUN_ERROR")
            
    """
    update database from output jsonl file which generated from evals framework
    """
    def update_evaluation_test_case_relation(self):
        try:
            actual_results = {}
            accuracy_results = {}
            line_number = 1
            with open(self.record_path, 'r') as f:
                for line in f:

                    line = line.strip()
                    data = json.loads(line)
                    eval_name = self.evaluation['eval']
                    if data.get('final_report'):
                        self.accuracy = data['final_report']['accuracy']
                    elif data.get('spec'):
                        self.run_id = data['spec']['run_id']
                    elif data.get('type') == 'sampling':
                        jsonl_order = data['sample_id'].split('.')[2]
                        sampled = data['data']['sampled']
                        actual_results[jsonl_order] = sampled
                    elif data.get('type') == 'match' and eval_name == 'match':
                        jsonl_order = data['sample_id'].split('.')[2]
                        matched = 1 if data['data']['correct'] else 0
                        accuracy_results[jsonl_order] = matched
                    elif data.get('type') == 'metrics':
                        jsonl_order = data['sample_id'].split('.')[2]
                        accuracy = data['data']['accuracy']
                        accuracy_results[jsonl_order] = accuracy
                    line_number += 1
                    
            for key in actual_results.keys():  
                    params = {}
                    params['actual_result'] = actual_results.get(str(key),None)
                    params['accuracy'] = accuracy_results.get(str(key),None)
                    params['jsonl_order'] = key
                    params['evaluation_id'] = self.params['evaluation_id']
                    EvaluationTestCaseRelation.update_evaluation_test_case_relation(params)
        except Exception as e:
            self.raise_error(str(e), "u_e_t_c_r_1" )
                

    """
    update evaluation table by setting status to COMPLETED and update accuracy and run_id

    @sets {Object} self.evaluation
    """
    def update_evaluation(self):
        try:
            self.evaluation = Evaluation.objects.get(id=self.params['evaluation_id'])
            self.evaluation.status = 'COMPLETED'
            self.evaluation.accuracy = self.accuracy
            self.evaluation.run_id = self.run_id
            self.evaluation.completed_at  = int(time.time())
            self.evaluation.save()
        except Exception as e:
            self.raise_error(str(e), "u_e_1" )
    
    """
    update evaluation table by setting status to FAILED and update error_object and retry_count

    @sets {Object} self.evaluation
    """
    def update_evaluation_on_error(self, error):
        self.evaluation = Evaluation.objects.get(id=self.params['evaluation_id'])
        self.evaluation.status = 'FAILED'
        self.evaluation.error_object = str(error)
        self.evaluation.initiated_at = 0
        self.evaluation.completed_at = 0
        
        self.evaluation.retry_count = int(self.evaluation.retry_count) + 1
        self.evaluation.evals_parameter = {}
        self.evaluation.save()
            
        
    """
    delete jsonl file and yaml file after evaluation or on error
    """
    def clean_up(self):
        try:
            if os.path.exists(self.record_path):
                os.remove(self.record_path)
                print(f"File '{self.record_path}' has been deleted successfully!")
            if os.path.exists(self.jsonl_file):
                os.remove(self.jsonl_file)
                print(f"File '{self.jsonl_file}' has been deleted successfully!")
            if os.path.exists(self.yaml_file):
                os.remove(self.yaml_file)
                print(f"File '{self.yaml_file}' has been deleted successfully!")
           
        except OSError as e:
            self.raise_error(str(e), 'c_u_1')
       
    def raise_error(self, message, code="bg_p_1", debug="SOMETHING_WENT_WRONG", ):
        error_data = {
            'message': message,
            'debug': debug,
            'code':code
        }
        
        raise Exception(error_data)
        
           


