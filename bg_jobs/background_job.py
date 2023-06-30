from bg_jobs.run_eval.main import RunEvalJob
import bg_jobs.globals as globals
import time

"""
Function to run a background job with given parameters.

@param {object} params
@param {string} params.evaluation_id
@param {string} params.prompt_template_id

@returns: Returns the error message if any, else None.
"""
def background_job(params):

    print('Sigint Triggered:::', globals.SIGINT_TRIGGERED)

    if not globals.SIGINT_TRIGGERED:
        globals.PROCESS_COMPLETED = False
        try:
            print(f"**********Background job started with given params {params['evaluation_id']}, {params['prompt_template_id']}**********")
            task = RunEvalJob(params)
            return task.perform()
        except Exception as e:
            return e
        finally:
            globals.PROCESS_COMPLETED = True
            print("Process Completed::: ", globals.PROCESS_COMPLETED)






