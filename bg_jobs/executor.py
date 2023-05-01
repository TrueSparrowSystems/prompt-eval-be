
import concurrent.futures
from bg_jobs.background_job import background_job


submitted_tasks = []
class SingletonThreadPoolExecutor(concurrent.futures.ThreadPoolExecutor):
    def __new__(cls):
        if not hasattr(cls, '_instance'):
            cls._instance = super().__new__(cls)
        return cls._instance

    # def execute(self, fn, *args):   
    #     print('In execute method    :',args, fn)  
    #     # if len(submitted_tasks) == 0:
    #     #     print('task array in if block   :', args)
    #     #     print('submitted_task array in if block   :', submitted_tasks)
    #     # else:
    #     #     for task in submitted_tasks:
    #     #         if args.index(task):
    #     #             args.remove(task)
    #     #     print('task array in else block   :', args)
    #     #     print('submitted_task array in else block   :', submitted_tasks)
    #     # submitted_tasks.extend(args)
    #     for arg in args:
    #         print("arg-----",arg)
    #         super().submit(fn, arg)
    
    def submit(self, background_job, *args, **kwargs):
        print('In submit method')
        super().submit(background_job, *args, **kwargs)


