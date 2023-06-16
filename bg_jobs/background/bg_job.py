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

class BgJob():
    def __init__(self, params):
        """
        Constructor for the BgJob class.

        @params: params: A dictionary containing the parameters for the background job.

        @return: None
        """
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
            print('Error while perform: ',str(e))
            self.update_evaluation_on_error(e)
            self.evaluation = Evaluation.objects.get(id=self.params['evaluation_id'])
            # delete all records from evaluation_test_case_relation table for this evaluation_id
            EvaluationTestCaseRelation.delete_records_by_evaluation_id(evaluation_id=self.params['evaluation_id'])
            self.clean_up()
            #check if retry_count is less than 3 and status is FAILED then retry
            if(self.evaluation.retry_count <= 3 and self.evaluation.status == Status['FAILED']):
                print('************* Retrying BGJOB Perform ****************')
                self.perform()
            else:
                print('************** Failed executing BG job after retries ****************')
                return str(e)
            
        
    def params_validation(self) :
        """
        check if evaluation_id or prompt_template_id is present in params
        """
        print('****************BGJOB params_validation ****************')
        if (not self.params.get('evaluation_id') and 
            not self.params.get('prompt_template_id')  
            ):
            self.raise_error("invalid params", "bg_j_b_bg_j_p_v_1")
            
    def update_evaluation_status(self):
        """
        update status of evaluation to RUNNING and update initiated_at
        """
        try:
            print('****************BGJOB update_evaluation_status ****************')
            self.evaluation = Evaluation.objects.get(id=self.params['evaluation_id'])
            if (self.evaluation['status'] != 'INITIATED'):
                self.evaluation.initiated_at  = int(time.time())
            self.evaluation.status = Status['RUNNING']
            self.evaluation.save()
        except Exception as e:
            print('error while updating status', str(e))
            self.raise_error(f"error while updating status:: {str(e)}", "bg_j_b_u_e_s_1")

            
    def fetch_testcases_by_prompt_template_id(self):
        """
        fetch testcases by prompt_template_id
        """
        try:
            self.test_cases = FetchTestCasesByPromptId(self.params).perform()
            if self.test_cases.count() == 0:
                self.raise_error("no test cases record found", "f_t_c_b_p_t_i_1")
        except Exception as e:
            self.raise_error(f"error while fetching test cases: {str(e)}", "f_t_c_b_p_t_i_2")
    
    def create_evaluation_test_case_relation(self):
        """
        create evaluation test case relation make entry in evaluation_test_case_relation table

        """
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
            
            print("insertObjects length:   ", len(insertObjects), insertObjects[0])
            EvaluationTestCaseRelation.bulk_create_evaluation_test_case_relation(insertObjects)  
        except Exception as e:
            self.raise_error(f"error while creating evaluation test case relation {str(e)}", "c_e_t_c_r_1")
        
    def create_prompt(self, testcase):
        """
        create prompt by replacing dynamic variables with values in prompt template by test case
        """
        prompt = CreatePrompt({
            'test_case': testcase, 
            'prompt_template_obj': self.prompt_template_obj
            }).perform()
                
        return prompt    
    
    def create_jsonl_file(self):
        """
        create input jsonl file for evals framework
        """
        try:
            self.evaluation_test_case_relation_records = EvaluationTestCaseRelation.objects.filter(
                evaluation_id=self.params['evaluation_id']
            ).order_by('jsonl_order')
            
            print('evaluation_test_case_relation_records:   ', self.evaluation_test_case_relation_records.count())
            
            jsonl_base_path = config('PE_JSONL_FOLDER_BASE_PATH')
            jsonl_folder_path = os.path.join(os.getcwd(), jsonl_base_path)
            if not os.path.exists(jsonl_folder_path):
                os.makedirs(jsonl_folder_path)
            unix_time = int(time.time())
            print('base_dir', os.getcwd())
            self.jsonl_file = os.path.join(jsonl_folder_path, str((self.params['evaluation_id'])) + '_' + str(unix_time) + '.jsonl')
            print('jsonl_file:   ', self.jsonl_file)
            with open(self.jsonl_file, mode='w') as output_jsonl:
                for evaluation_test_case_relation_record in self.evaluation_test_case_relation_records:
                    prompt = evaluation_test_case_relation_record['prompt']
                    acceptable_result = evaluation_test_case_relation_record['acceptable_result']
                    data = {'input': prompt, 'ideal': acceptable_result}
                    print('data:   ', data)
                    json.dump(data, output_jsonl)
                    output_jsonl.write('\n')
        except Exception as e:
            print("Error while creating jsonl file: ", str(e))
            self.raise_error(str(e), "c_j_f_1")
 
    def create_yaml_file(self):
        """
        create ymal file for choosing evaluator for evals framework
        build new ymal file from base ymal file according to eval name
        """
        try:
            self.yaml_folder = os.path.join(os.getcwd(), config('PE_YAML_FOLDER_BASE_PATH'))
            self.eval_folder = os.path.join(self.yaml_folder, 'evals')
            
            unix_time = int(time.time())
            if not os.path.exists(self.yaml_folder):
                os.mkdir(self.yaml_folder)
                
            if not os.path.exists(self.eval_folder):
                os.mkdir(self.eval_folder)

            self.yaml_file = os.path.join(self.eval_folder, str(self.params['evaluation_id']) + '_' + str(unix_time) + '.yaml')
            print('yaml_file:   ', self.yaml_file)  
                
            base_yaml_file = os.path.join(self.yaml_folder, 'base.yaml')
            print('base_yaml_file:   ', base_yaml_file)
            
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

            print('eval_name:   evaluation_id:  version:    class_name:     jsonl_file_path:', eval_name, evaluation_id, version, class_name, jsonl_file_path)
            
            with open(base_yaml_file, "r") as file:
                # Load the YAML contents into a Python dictionary
                yaml_dict = yaml.load(file, Loader=yaml.FullLoader)
                print('yaml_dict-----', yaml_dict)
                if eval_name != 'graphql':
                    # Remove the two lines from the dictionary
                    del yaml_dict['eval_name.evaluation_id.version']['args']['fuzzy']
                    del yaml_dict['eval_name.evaluation_id.version']['args']['extract_gql']
                yaml_str = yaml.dump(yaml_dict)
                print('yaml_str-----', yaml_dict)
                yaml_str = yaml_str.replace("eval_name", eval_name)
                yaml_str = yaml_str.replace("evaluation_id", str(evaluation_id))
                yaml_str = yaml_str.replace("version", version)
                yaml_str = yaml_str.replace("metrics_list", "[accuracy]")
                yaml_str = yaml_str.replace("class_name", class_name)
                yaml_str = yaml_str.replace("jsonl_file_path", jsonl_file_path)
                yaml_str = yaml_str.replace("fuzzy_boolean", str(fuzzy_boolean))
                yaml_str = yaml_str.replace("extract_gql_boolean", str(extract_gql_boolean))
                print('yaml_str after replacement-----', yaml_str)

            with open(self.yaml_file, "w") as file:
                file.write(yaml_str)
        except Exception as e:
            print("Error while creating yaml file: ", e)
            self.raise_error(str(e), "c_y_f_1" )


    def update_evals_parameter(self):  
        """
        update evals parameter in evaluation table
        """
        try:
            self.evaluation = Evaluation.objects.get(id=self.params['evaluation_id'])
            self.evaluation.eval_parameter = {
                'jsonl_file_path': self.jsonl_file,
                'yaml_file_path': self.yaml_file
            }
            self.evaluation.save()
        except Exception as e:
            print("Error while updating files in evaluation db: ", str(e))
            self.raise_error(str(e), "u_e_p_1" )
                
    def run_evaluation(self):
        """
        run evaluation using CLI by making command which take jsoln file and ymal file as input
        """
        try:
            
            completion_fn = self.evaluation['model']
            eval = self.evaluation['eval'] + '.' + str(self.params['evaluation_id'])
            self.record_path = os.path.join(self.eval_folder, f"output_{str(self.params['evaluation_id'])}.jsonl")
            registry_path = self.yaml_folder
            
            # completion_fn = 'gpt-3.5-turbo'
            # eval = 'graphql.6453a63ea80680d9183b7d6b'
            # self.record_path = '/Users/shraddha/git/prompt-eval-be/YAML/evals/output.jsonl'
            # registry_path = '/Users/shraddha/git/prompt-eval-be/YAML'
            print('completion_fn:   ', completion_fn)
            print('eval:   ', eval)
            print('record_path:   ', self.record_path)
            print('registry_path:   ', registry_path)
            
            # Using command
            
            # args = EvalArguments(
            #     extra_eval_params='',
            #     max_samples=None,
            #     cache=True,
            #     visible='',
            #     user='',
            #     completion_fn='gpt-3.5-turbo',
            #     eval='graphql-fuzzy',
            #     seed=20220722,
            #     record_path='/Users/shraddha/git/prompt-eval-be/JSONL/output.jsonl',
            #     registry_path=['/Users/shraddha/git/prompt-eval-be/YAML'],
            #     debug=True,
            #     local_run=True,
            #     dry_run_logging=True
            # )
            
            # oaieval.run(args)
            # print('Execution ended::')
            
            # Using CLI

            command = f"oaieval {completion_fn} {eval} --debug --registry_path {registry_path} --record_path {self.record_path}"
            print('command--------', command)
            with subprocess.Popen(command.split(), stdout=subprocess.PIPE, bufsize=1, universal_newlines=True) as p:
                for line in p.stdout:
                    print(line, end='')

        except Exception as e:
            print('Error while running evals:   ', str(e))
            self.raise_error(str(e), "bg_j_b_bg_j_r_e_1", "EVALS_RUN_ERROR")
            
    def update_evaluation_test_case_relation(self):
        """
        update database from output jsonl file which generated from evals framework
        """
        try:
            actual_results = {}
            accuracy_results = {}
            line_number = 1
            with open(self.record_path, 'r') as f:
                for line in f:

                    line = line.strip()
                    print("\n\nbefore load",)
                    data = json.loads(line)
                    print("\n\n",line_number)
                    eval_name = self.evaluation['eval']
                    if data.get('final_report'):
                        print('Inside final report:')
                        self.accuracy = data['final_report']['accuracy']
                    elif data.get('spec'):
                        print('Inside spec :')
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
                    
            print("line_number:   ", line_number)
            print("actual_results:   ", actual_results, len(actual_results))
            print("accuracy_results:   ", accuracy_results, len(accuracy_results))
                    
            for key in actual_results.keys():  
                    params = {}
                    params['actual_result'] = actual_results.get(str(key),None)
                    params['accuracy'] = accuracy_results.get(str(key),None)
                    params['jsonl_order'] = key
                    params['evaluation_id'] = self.params['evaluation_id']
                    print("params:   ", params)
                    EvaluationTestCaseRelation.update_evaluation_test_case_relation(params)
        except Exception as e:
            self.raise_error(str(e), "u_e_t_c_r_1" )
                

    def update_evaluation(self):
        """
        update evaluation table by setting status to COMPLETED and update accuracy and run_id
        """
        try:
            self.evaluation = Evaluation.objects.get(id=self.params['evaluation_id'])
            self.evaluation.status = 'COMPLETED'
            self.evaluation.accuracy = self.accuracy
            self.evaluation.run_id = self.run_id
            self.evaluation.completed_at  = int(time.time())
            self.evaluation.save()
        except Exception as e:
            self.raise_error(str(e), "u_e_1" )
    
    def update_evaluation_on_error(self, error):
        """
        update evaluation table by setting status to FAILED and update error_object and retry_count
        """
        self.evaluation = Evaluation.objects.get(id=self.params['evaluation_id'])
        self.evaluation.status = 'FAILED'
        self.evaluation.error_object = str(error)
        self.evaluation.initiated_at = 0
        self.evaluation.completed_at = 0
        
        self.evaluation.retry_count = int(self.evaluation.retry_count) + 1
        self.evaluation.evals_parameter = {}
        self.evaluation.save()
            
        
    def clean_up(self):
        """
        delete jsonl file and yaml file after evaluation or on error
        """
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
        
           


