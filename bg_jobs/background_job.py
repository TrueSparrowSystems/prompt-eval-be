from bg_jobs.background.bg_job import BgJob
import time
import signal

stop_requested = False

def handle_sigint(signal_num, frame):
    global stop_requested
    stop_requested = True
    print("SIGINT received. Stopping background task...")

def background_job(params):
    # Register the SIGINT signal handler
    signal.signal(signal.SIGINT, handle_sigint)

    # Start the background task
    while not stop_requested:
        try:
            print(f"**********Background job started with given params {params['evaluation_id']}, {params['prompt_template_id']}**********")
            #task = BgJob(params)
            #return task.perform()
            print("Started sleeping")
            time.sleep(1)
            print("Sleeping done")
        except Exception as e:
            print("error while executing BG job------", e)
            return e

    signal.signal(signal.SIGINT, signal.SIG_DFL)
