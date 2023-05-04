from django.test import TestCase
from graphQL.db_models.prompt_template import PromptTemplate
from graphQL.db_models.test_case import TestCase as tc
from graphQL.db_models.experiment import Experiment
from graphQL.db_models.evaluation import Evaluation
from graphQL.db_models.evaluation_test_case_relation import EvaluationTestCaseRelation
from bg_jobs.background_job import background_job

import time

class TestBgJob(TestCase):
    
    def test_bg_job(self):
        pass
        # Todo: uncomment this once bg job integrated
        # Write a code to create experiment
        # experiment = Experiment.objects.create(name="Test Experiment", description="This is a test experiment",
        #                                        dynamic_vars= ['name', 'age'])
        # print(experiment.id)
        # # Write a code to create prompt template
        # prompt_template = PromptTemplate.objects.create(name="Test Prompt", 
        #                               description="This is a test prompt", 
        #                               experiment_id=experiment.id,
        #                               conversation= [{
        #                                   'role': 'USER',
        #                                   'content': ' Hi, how are you {name}?'
        #                               }, {
        #                                   'role': 'ASSISTANT',
        #                                   'content': 'Hello, May I know your age?'
        #                               }, {
        #                                   'role': 'USER',
        #                                   'content': 'sure, i am {age} years old.'
        #                               }])
        # print(prompt_template.id)
        # test_case_1 = tc.objects.create(name="Test Case",
        #                                     description="This is a test case",
        #                                     dynamic_var_values={"name": "John", "age": "20"},
        #                                     experiment_id=experiment.id)
        # print(test_case_1.id)
        # test_case_2 = tc.objects.create(name="Test Case",
        #                                     description="This is a test case",
        #                                     dynamic_var_values={"name": "John", "age": "20"},
        #                                     experiment_id=experiment.id)
        # print(test_case_2.id)
        
        # evaluation = Evaluation.objects.create(model="gpt-3.5-turbo",
        #                                                           eval="regex-match",
        #                                                           prompt_template_id=prompt_template.id,
        #                                                           status="INITIATED",
        #                                                           initiated_at=int(time.time()))
        # print(evaluation.id)
        
        # background_job({'evaluation_id': evaluation.id, 'prompt_template_id': prompt_template.id})
                                                                  
        # #delete records after test case passes
        # Experiment.objects.filter(id=experiment.id).delete()
        # PromptTemplate.objects.filter(id=prompt_template.id).delete()
        # tc.objects.filter(id=test_case_1.id).delete()
        # tc.objects.filter(id=test_case_2.id).delete()
        # Evaluation.objects.filter(id=evaluation.id).delete()
        # EvaluationTestCaseRelation.objects.filter(evaluation_id=evaluation.id).delete()
        

        