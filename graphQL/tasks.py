from celery import Task
from api.celery import app

class BgJob(Task):

    def __init__(self, x,y):
        self.x = x
        self.y = y

    def perform(self, x, y):
        try:
            c = x+y
            print("c------", c)
            return c
        except Exception as e:
            print("e------", e)
            return False

# Register MyClassTask with Celery
@app.task
def backgroundTask(x, y):
    try:
        task = BgJob(x, y)
        return task.perform(x, y)
    except Exception as e:
        print("error while executing BG job------", e)
        return e