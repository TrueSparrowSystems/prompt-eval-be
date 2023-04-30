from bg_jobs.background.bg_job import BgJob
import time

def background_job(params):
    try:
        print(f"**********Background job started with given params {params['evaluation_id']}, {params['prompt_template_id']}**********")
        # task = BgJob(params)
        # return task.perform()
        time.sleep(5)
        print("done")
    except Exception as e:
        print("error while executing BG job------", e)
        return e

    