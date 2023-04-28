from bg_jobs.background.bg_job import BgJob

def background_job(params):
    try:
        print(f"**********Background job started with given params {params['evaluation_id']}, {params['prompt_template_id']}**********")
        task = BgJob(params)
        return task.perform()
    except Exception as e:
        print("error while executing BG job------", e)
        return e

    