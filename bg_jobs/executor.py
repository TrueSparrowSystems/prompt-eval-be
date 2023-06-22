
import concurrent.futures
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
        if len(self.submitted_tasks) != 0 and fn_args in self.submitted_tasks:
            return
                    
        self.submitted_tasks.append(fn_args)
        super().submit(fn, fn_args)
    
   


