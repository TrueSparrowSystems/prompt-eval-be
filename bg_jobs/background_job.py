from bg_jobs.background.bg_job import BgJob
import bg_jobs.globals as globals
import time

def background_job(params):
    print('Sigint Triggered::: ', globals.SIGINT_TRIGGERED)

    if not globals.SIGINT_TRIGGERED:
        globals.PROCESS_COMPLETED = False
        try:
            print(f"**********Background job started with given params {params['evaluation_id']}, {params['prompt_template_id']}**********")
            task = BgJob(params)
            return task.perform()
        except Exception as e:
            return e
        finally:
            globals.PROCESS_COMPLETED = True
            print("Process Completed::: ", globals.PROCESS_COMPLETED)
            
    
        
 
        

