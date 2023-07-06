from graphQL.db_models.evaluation_test_case_relation import EvaluationTestCaseRelation
from graphQL.db_models.evaluation import Evaluation, Status
from graphQL.db_models.prompt_template import PromptTemplate
from .create_eval_files import CreateEvalFiles
from .fetch_test_cases import FetchTestCasesByPromptId
from .create_prompt import CreatePrompt
from decouple import config
import json, time
import subprocess
import os
import logging

ACCURACY_THRESHOLD_FOR_PASSING = 0.6

"""
bg job class which perform background job for evaluation

@class BgJob
"""
class RunEvalJob():
    """
    Constructor for the BgJob class.

    @params {Object} params
    @params {String} params.evaluation_id
    @params {String} params.prompt_template_id
    """
    def __init__(self, params):
        self.params = params
        self.eval = ''
        self.created_files = []
        self.jsonl_file = ''
        self.yaml_file = ''
        self.accuracy = 0
        self.run_id = 0
        self.total_testcases = 0
        self.passed_testcases = 0

    def perform(self):
        try:
            print('****************BGJOB Perform ****************')

            self.params_validation()

            self.update_evaluation_status()

            # TODO: Fetching test cases and creating evaluation test case relation can be same lib
            self.fetch_testcases_by_prompt_template_id()

            self.create_evaluation_test_case_relation()

            self.create_eval_files()

            # TODO: There is no need for eval_parameter column in evaluations. And hence no need for this function.
            self.update_evals_parameter()

            self.run_evaluation()

            # # TODO: A separate method to parse the results and the update the evaluation test case relation table based on the results
            self.update_evaluation_test_case_relation()

            self.update_evaluation()

            self.clean_up()

        except Exception as e:
            logging.error("ERROR:::::::::::::", e)

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
        # TODO: This method should set evaluation in self and validate if to run the evaluation. And also update its status to RUNNING(merge update_evaluation_status method)
        print('****************BGJOB params_validation ****************')
        if (not self.params.get('evaluation_id') and
            not self.params.get('prompt_template_id')
            ):
            self.raise_error("invalid params", "bg_j_b_bg_j_p_v_1")

    """
    Update evaluation status to RUNNING

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
    Fetch Test Cases by prompt template id

    @sets {Object} self.test_cases
    """
    def fetch_testcases_by_prompt_template_id(self):
        try:
            self.test_cases = FetchTestCasesByPromptId(self.params).perform()
            self.total_testcases = self.test_cases.count()
            if self.total_testcases == 0:
                self.raise_error("no test cases record found", "f_t_c_b_p_t_i_1")
        except Exception as e:
            self.raise_error(f"error while fetching test cases: {str(e)}", "f_t_c_b_p_t_i_2")

    """
    Create records in evaluation test case relation table

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
    Create prompt for each test case

    @params {Object} testcase

    @returns {Object} prompt
    """
    def create_prompt(self, testcase):
        prompt = CreatePrompt({
            'test_case': testcase,
            'prompt_template_obj': self.prompt_template_obj
            }).perform()

        return prompt

    def create_eval_files(self):
        createEvalFilesResp = CreateEvalFiles({
            'evaluation': self.evaluation
        }).perform()

        self.eval = createEvalFilesResp['eval']
        self.created_files = createEvalFilesResp['files_created']
        self.jsonl_file = createEvalFilesResp['jsonl_file']
        self.yaml_file = createEvalFilesResp['yaml_file']


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
    run evaluation using CLI by making command which take jsonl file and yaml file as input

    @sets {Object} self.evaluation
    """
    def run_evaluation(self):
        try:
            yaml_folder = os.path.join(os.getcwd(), config('PE_YAML_FOLDER_BASE_PATH'))
            eval_folder = os.path.join(yaml_folder, 'evals')

            completion_fn = self.evaluation['model']
            self.record_path = os.path.join(eval_folder, f"output_{str(self.params['evaluation_id'])}.jsonl")
            registry_path = yaml_folder

            self.created_files.append(self.record_path)

            command = f"oaieval {completion_fn} {self.eval} --debug --registry_path {registry_path} --record_path {self.record_path}"

            calling_output = subprocess.run(command.split(), capture_output=True)
            exitcode = calling_output.returncode

            if exitcode != 0:
                errLogBasePath = config("PE_ERROR_LOG_FOLDER_BASE_PATH")
                errLogFolderPath = os.path.join(os.getcwd(), errLogBasePath)
                if not os.path.exists(errLogFolderPath):
                    os.makedirs(errLogFolderPath)
                unix_time = int(time.time())

                errLogFile = os.path.join(
                    errLogFolderPath,
                    str(self.params['evaluation_id']) + "_" + str(unix_time) + ".log",
                )
                print(" ",errLogFile)

                with open(errLogFile, "wb") as err_log_file:
                    # Write bytes to file
                    err_log_file.write(calling_output.stderr)   
    
                raise ValueError('Something went wrong while running evaluation. Please check the logs at, ', errLogFile, ' for more details.')

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
            processed_sample_ids = []
            with open(self.record_path, 'r') as f:
                for line in f:

                    line = line.strip()
                    data = json.loads(line)

                    eval_name = self.evaluation['eval']
                    if data.get('final_report'):
                        if 'accuracy' in data['final_report'].keys():
                            self.accuracy = data['final_report']['accuracy']
                        elif 'score' in data['final_report'].keys():
                            self.accuracy = data['final_report']['score']
                        else:
                            self.raise_error("accuracy not found in final report", "u_e_t_c_r_2")
                    elif data.get('spec'):
                        self.run_id = data['spec']['run_id']
                    elif data.get('type') == 'sampling':
                        jsonl_order = data['sample_id'].split('.')[2]
                        sampled = data['data']['sampled']
                        # This has specifically been added for model-graded evals, as there are multiple entries created for model-graded evals
                        # The first entry is the actual result and the second entry is from the prompt provided by model-graded.
                        actual_results[jsonl_order] = sampled if data['sample_id'] not in processed_sample_ids else actual_results[jsonl_order]
                        processed_sample_ids.append(data['sample_id'])
                    elif data.get('type') == 'match' and eval_name == 'match':
                        jsonl_order = data['sample_id'].split('.')[2]
                        matched = 1 if data['data']['correct'] else 0
                        accuracy_results[jsonl_order] = matched
                    elif data.get('type') == 'metrics':
                        jsonl_order = data['sample_id'].split('.')[2]
                        if 'accuracy' in data['data'].keys():
                            accuracy = data['data']['accuracy']
                        elif 'score' in data['data'].keys():
                            accuracy = data['data']['score']
                        else:
                            self.raise_error("accuracy not found in final report", "u_e_t_c_r_3")
                        accuracy_results[jsonl_order] = accuracy
                    line_number += 1

            for key in actual_results.keys():
                    params = {}
                    params['actual_result'] = actual_results.get(str(key),None)
                    params['accuracy'] = accuracy_results.get(str(key),None)
                    if params['accuracy'] >= ACCURACY_THRESHOLD_FOR_PASSING:
                        self.passed_testcases += 1
                    params['jsonl_order'] = key
                    params['evaluation_id'] = self.params['evaluation_id']
                    EvaluationTestCaseRelation.update_evaluation_test_case_relation(params)
        except Exception as e:
            self.raise_error(str(e), "u_e_t_c_r_1" )


    """
    Update evaluation status to COMPLETED and update accuracy and run_id

    @sets {Object} self.evaluation
    """
    def update_evaluation(self):
        try:
            self.evaluation = Evaluation.objects.get(id=self.params['evaluation_id'])
            self.evaluation.status = 'COMPLETED'
            self.evaluation.accuracy = self.accuracy
            self.evaluation.passed_testcases = self.passed_testcases
            self.evaluation.total_testcases = self.total_testcases
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
            for file_path in self.created_files:
                if os.path.exists(file_path):
                    os.remove(file_path)
                    print(f"File '{file_path}' has been deleted successfully!")

        except OSError as e:
            self.raise_error(str(e), 'c_u_1')

    def raise_error(self, message, code="bg_p_1", debug="SOMETHING_WENT_WRONG", ):
        logging.error(message)
        error_data = {
            'message': message,
            'debug': debug,
            'code':code
        }

        raise Exception(error_data)




