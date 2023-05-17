from bg_jobs.background.bg_job import BgJob
import bg_jobs.globals as globals
import time

def background_job(params):
    print('sigint_triggered:::', globals.SIGINT_TRIGGERED)

    if not globals.SIGINT_TRIGGERED:
        globals.PROCESS_COMPLETED = False
        try:
            print(f"**********Background job started with given params {params['evaluation_id']}, {params['prompt_template_id']}**********")
            task = BgJob(params)
            return task.perform()
            time.sleep(1)
            print(f"Sleeping done {params['evaluation_id']}, {params['prompt_template_id']}")
        except Exception as e:
            print("error while executing BG job------", e)
            return e
        finally:
            globals.PROCESS_COMPLETED = True
            print("process_completed:::", globals.PROCESS_COMPLETED)
            
    
        
 
        

