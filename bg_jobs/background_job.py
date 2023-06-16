from bg_jobs.background.bg_job import BgJob
import bg_jobs.globals as globals
import time

def background_job(params):
    """
    Function to run a background job with given parameters.
    @params: Dictionary containing the parameters for the background job.
    @return: The result of the background job execution or an exception if an error occurs.
    """
    
    # Print the value of the global variable SIGINT_TRIGGERED
    print('sigint_triggered:::', globals.SIGINT_TRIGGERED)

    # Check if SIGINT_TRIGGERED is False
    if not globals.SIGINT_TRIGGERED:
        globals.PROCESS_COMPLETED = False
        try:
            # Print a message indicating the start of the background job with the given params
            print(f"**********Background job started with given params {params['evaluation_id']}, {params['prompt_template_id']}**********")
            # Create an instance of the BgJob class and perform the task
            task = BgJob(params)
            return task.perform()
            time.sleep(1)
            print(f"Sleeping done {params['evaluation_id']}, {params['prompt_template_id']}")
        except Exception as e:
            # Print an error message if an exception occurs during the execution of the background job
            print("error while executing BG job------", e)
            return e
        finally:
            # Set the global variable PROCESS_COMPLETED to True
            globals.PROCESS_COMPLETED = True
            print("process_completed:::", globals.PROCESS_COMPLETED)
            
    
        
 
        

