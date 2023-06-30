from django.test import TestCase
from graphQL.db_models.prompt_template import PromptTemplate
from graphQL.db_models.test_case import TestCase as tc
from graphQL.db_models.experiment import Experiment
from bg_jobs.run_eval.fetch_test_cases import FetchTestCasesByPromptId

class FetchTestCasesByPromptIdTest(TestCase):

    def test_fetch_test_cases(self):
        # Write a code to create experiment
        experiment = Experiment.objects.create(name="Test Experiment", description="This is a test experiment",
                                               dynamic_vars= ['name', 'age'])
        print(experiment.id)
        # Write a code to create prompt template
        prompt_template = PromptTemplate.objects.create(name="Test Prompt",
                                      description="This is a test prompt",
                                      experiment_id=experiment.id,
                                      conversation= [{
                                          'role': 'user',
                                          'content': ' Hi, how are you {name}?, what is your {age} ?'
                                      }])
        print(prompt_template.id)
        # Write a code to create test case
        test_case = tc.objects.create(name="Test Case",
                                            description="This is a test case",
                                            dynamic_var_values={"name": "John", "age": "20"},
                                            experiment_id=experiment.id)
        print(test_case.id)
        test_cases = FetchTestCasesByPromptId({
            'prompt_template_id': prompt_template.id
            }).perform()

        #delete experiment, prompt_template, test_case
        print('test_cases: ', test_cases.count())
        test_cases_count = test_cases.count()
        Experiment.objects.filter(id=experiment.id).delete()
        PromptTemplate.objects.filter(id=prompt_template.id).delete()
        tc.objects.filter(id=test_case.id).delete()
        self.assertEqual(test_cases_count, 1)
