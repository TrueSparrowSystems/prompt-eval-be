from graphQL.db_models.evaluation_test_case_relation import EvaluationTestCaseRelation
from decouple import config
import yaml
from bg_jobs.globals import EVALS_BASE_FILE_DICT, MODEL_GRADED_EVALS
import json, time
import os
import logging

class CreateEvalFiles:
    def __init__(self, params):
        self.params = params
        self.evaluation = params["evaluation"]
        self.evaluation_test_case_relation_records = []
        self.yaml_folder_path = ""
        self.eval_folder_path = ""
        self.yaml_file_path = ""
        self.jsonl_file_path = ""

    def perform(self):

        self.create_jsonl_file()

        self.create_yaml_file()

        return { 'files_created': [self.jsonl_file_path, self.yaml_file_path], 'eval': self.eval, 'jsonl_file': self.jsonl_file_path, 'yaml_file': self.yaml_file_path, 'yaml_file': self.yaml_file_path}

    """
  Create input jsonl file for evals framework

  @sets {Object} self.evaluation_test_case_relation_records
  """

    def create_jsonl_file(self):
        try:
            self.evaluation_test_case_relation_records = (
                EvaluationTestCaseRelation.objects.filter(
                    evaluation_id=self.evaluation["id"]
                ).order_by("jsonl_order")
            )

            jsonl_base_path = config("PE_JSONL_FOLDER_BASE_PATH")
            jsonl_folder_path = os.path.join(os.getcwd(), jsonl_base_path)
            if not os.path.exists(jsonl_folder_path):
                os.makedirs(jsonl_folder_path)
            unix_time = int(time.time())

            self.jsonl_file_path = os.path.join(
                jsonl_folder_path,
                str((self.evaluation["id"])) + "_" + str(unix_time) + ".jsonl",
            )

            with open(self.jsonl_file_path, mode="w") as output_jsonl:
                for (
                    evaluation_test_case_relation_record
                ) in self.evaluation_test_case_relation_records:
                    prompt = evaluation_test_case_relation_record["prompt"]
                    acceptable_result = evaluation_test_case_relation_record[
                        "acceptable_result"
                    ]
                    data = {"input": prompt, "ideal": acceptable_result}

                    json.dump(data, output_jsonl)
                    output_jsonl.write("\n")
        except Exception as e:
            self.raise_error(str(e), "c_j_f_1")

    """
  Create yaml file for choosing evaluator for evals framework
  Build new yaml file from base yaml file according to eval name

  @sets {Object} self.yaml_file_path
  """

    def create_yaml_file(self):
        try:
            self.yaml_folder_path = os.path.join(
                os.getcwd(), config("PE_YAML_FOLDER_BASE_PATH")
            )
            self.eval_folder_path = os.path.join(self.yaml_folder_path, "evals")
            unix_time = int(time.time())
            if not os.path.exists(self.yaml_folder_path):
                os.mkdir(self.yaml_folder_path)

            if not os.path.exists(self.eval_folder_path):
                os.mkdir(self.eval_folder_path)

            self.yaml_file_path = os.path.join(
                self.eval_folder_path,
                str(self.evaluation["id"]) + "_" + str(unix_time) + ".yaml",
            )

            eval_name = self.evaluation["eval"]
            evaluation_id = self.evaluation["id"]
            jsonl_file_path = self.jsonl_file_path

            self.eval = eval_name + "_" + str(evaluation_id) + "_" + str(unix_time)

            yaml_base_file_path = EVALS_BASE_FILE_DICT[eval_name]
            with open(yaml_base_file_path, "r") as file:
                yaml_dict = yaml.load(file, Loader=yaml.FullLoader)
                yaml_str = yaml.dump(yaml_dict)
                yaml_str = yaml_str.replace("eval_name_placeholder", self.eval)
                yaml_str = yaml_str.replace(
                    "jsonl_file_path_placeholder", jsonl_file_path
                )

            with open(self.yaml_file_path, "w") as file:
                file.write(yaml_str)

        except Exception as e:
            self.raise_error(str(e), "c_y_f_1")

    def raise_error(self, message, code="bg_j_b_cp", debug="SOMETHING_WENT_WRONG"):
        logging.error(message)
        error_data = {"message": message, "debug": debug, "code": code}

        raise Exception(error_data)
