
import concurrent.futures
from bg_jobs.background_job import background_job
from decouple import config


class SingletonThreadPoolExecutor(concurrent.futures.ThreadPoolExecutor):
    def __new__(cls, ):
        if not hasattr(cls, '_instance'):
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        super().__init__(int(config('PE_MAX_WORKERS')))
        self.submitted_tasks = []

    def submit(self, fn, fn_args):  
        print('task array   :', fn_args) 
        print('self.submitted_tasks   :', self.submitted_tasks)
        if len(self.submitted_tasks) != 0 and fn_args in self.submitted_tasks:
            print('task array in else block   :', fn_args)
            print('submitted_task array in else block   :', self.submitted_tasks)
            return
                    
        self.submitted_tasks.append(fn_args)
        super().submit(fn, fn_args)
    
   

