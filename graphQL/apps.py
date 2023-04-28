from django.apps import AppConfig
from django.conf import settings
from bg_jobs.background_job import background_job
from bg_jobs.executor import executor
from graphQL.db_models.evaluation import Evaluation


class GraphqlConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "graphQL"

    def ready(self):
        params = {'p1': 'initial', 'p2': 'initial'}
        print(' I am here---------')
        all_evaluations = Evaluation.objects.all()
        for evaluation in all_evaluations:
            print('Evaluation_id-------', evaluation.id)

        executor.submit(background_job, params)
        # tasks = executor.get_queue()
        # print('tasks-------', tasks)
        # params = {'p1': 'initial2', 'p2': 'initial2'}

        # # before submit write a code to get what are the tasks present in bg job tasks
        # executor.submit(background_job, params)
        
        
       

