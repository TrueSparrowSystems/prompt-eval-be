from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView
from bg_jobs.executor import SingletonThreadPoolExecutor
from bg_jobs.background_job import background_job

urlpatterns = [
    path(
        "", csrf_exempt(GraphQLView.as_view(graphiql=True))
    )
]

def on_startup():
    
    bg_params = [
    {
        "evaluation_id": "1234",
        "prompt_template_id": "1234"
    },
    { 
        "evaluation_id": "12345",
        "prompt_template_id": "12345"
    },
        { 
        "evaluation_id": "12345",
        "prompt_template_id": "12345"
    }
    
    ]
    
    if (len(bg_params) > 0):
        executor = SingletonThreadPoolExecutor()
        for bg_param in bg_params:
            print('bg_param------',bg_param)
            executor.submit(background_job, bg_param)

on_startup()
