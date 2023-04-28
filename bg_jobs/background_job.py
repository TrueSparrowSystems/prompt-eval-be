import time

def background_job(params):
    print(f"**********Background job started with given params {params['evaluation_result_id']}, {params['prompt_template_id']}**********     :")
    print("Background job finished")
