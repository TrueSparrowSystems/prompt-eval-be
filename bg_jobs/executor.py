
import concurrent.futures

submitted_tasks = []
class SingletonThreadPoolExecutor(concurrent.futures.ThreadPoolExecutor):
    def __new__(cls):
        if not hasattr(cls, '_instance'):
            cls._instance = super().__new__(cls)
        return cls._instance

    def execute(self, fn, *args):   
        print('In execute method    :',args)  
        # if len(submitted_tasks) == 0:
        #     print('task array in if block   :', args)
        #     print('submitted_task array in if block   :', submitted_tasks)
        # else:
        #     for task in submitted_tasks:
        #         if args.index(task):
        #             args.remove(task)
        #     print('task array in else block   :', args)
        #     print('submitted_task array in else block   :', submitted_tasks)
        # submitted_tasks.extend(args)
        return super().map(fn, *args)
    
    # def submit(self, fn, *args, **kwargs):
    #     print('In execute method    :',args)  
    #     if len(submitted_tasks) == 0:
    #         print('task array in if block   :', args)
    #         print('submitted_task array in if block   :', submitted_tasks)
    #         submitted_tasks.append(args)
    #     else:
    #         for task in submitted_tasks:
    #             if args.index(task):
    #                 #args.remove(task)
    #                 return
    #         submitted_tasks.append(args)
    #         print('task array in else block   :', args)
    #         print('submitted_task array in else block   :', submitted_tasks)
         
    #     print('In submit method')
    #     return super().submit(fn, *args, **kwargs)


