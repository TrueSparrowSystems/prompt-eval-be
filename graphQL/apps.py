from django.apps import AppConfig
from django.conf import settings
from bg_jobs.executor import SingletonThreadPoolExecutor
from bg_jobs.background_job import background_job

submitted_task = []
class GraphqlConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "graphQL"

    def ready(self):
        array = [
        {
            "evaluation_id": "1234",
            "prompt_template_id": "1234"
        },
        { 
            "evaluation_id": "12345",
            "prompt_template_id": "12345"
        }
        ]
        
        executor = SingletonThreadPoolExecutor()
        #executor.execute(background_job, array)

        if len(submitted_task) != 0:
            for task in submitted_task:
                if array.index(task):
                    array.remove(task)
            print('task array in if block   :', array)
            print('submitted_task array in if block   :', submitted_task)
        executor.execute(background_job, array)

            
# fidnd error on above code

        
        
       

