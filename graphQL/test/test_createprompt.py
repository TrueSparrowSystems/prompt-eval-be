from django.test import TestCase
from graphQL.db_models.prompt_template import PromptTemplate
from graphQL.db_models.test_case import TestCase as tc
from graphQL.db_models.experiment import Experiment
from bg_jobs.background.create_prompt import CreatePrompt

class CreatePromptTest(TestCase):

    def test_create_prompt(self):
        # Write a code to create experiment
        experiment = Experiment.objects.create(name="Test Experiment", description="This is a test experiment")
        print(experiment.id)
        # Write a code to create prompt template
        prompt_template = PromptTemplate.objects.create(name="Test Prompt",
                                      description="This is a test prompt",
                                      experiment_id=experiment.id,
                                      conversation= [{
                                          'role': 'user',
                                          'content': ' Hi, how are you {name}?'
                                      }])
        print(prompt_template.id)
        # Write a code to create test case
        test_case = tc.objects.create(name="Test Case",
                                            description="This is a test case",
                                            dynamic_var_values={"name": "John"},
                                            experiment_id=experiment.id)
        print(test_case.id)
        testcase = tc.test_case_by_id(test_case.id)
        prompt_template = PromptTemplate.prompt_by_id(prompt_template.id)

        prompt = CreatePrompt({
            'test_case': testcase,
            'prompt_template_obj': prompt_template
            }).perform()

        #delete experiment, prompt_template, test_case
        Experiment.objects.filter(id=experiment.id).delete()
        PromptTemplate.objects.filter(id=prompt_template.id).delete()
        tc.objects.filter(id=test_case.id).delete()

        self.assertEqual(prompt, [{'role': 'user', 'content': ' Hi, how are you John?'}] )
