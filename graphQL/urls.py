from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView
from bg_jobs.startup import startup

urlpatterns = [
    path(
        "", csrf_exempt(GraphQLView.as_view(graphiql=True))
    )
]

def on_startup():
    startup()
    
on_startup()
