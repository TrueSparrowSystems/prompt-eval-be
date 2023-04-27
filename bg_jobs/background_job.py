import time

def background_job(params):
    print("Background job started", params['p1'], params['p2'])
    time.sleep(5)  # simulate a long-running task
    print("Background job finished")
