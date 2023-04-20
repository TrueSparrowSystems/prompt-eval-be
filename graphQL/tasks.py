# tasks.py
import time

from celery import shared_task

@shared_task
def add(x, y):
    print('sleepng')
    time.sleep(10)
    print('done ')
    return x + y
