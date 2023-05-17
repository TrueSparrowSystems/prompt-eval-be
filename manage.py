#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import signal
import time
import bg_jobs.globals as globals



def handle_sigint(signal_num, frame):
    #global sigint_triggered
    #sigint_triggered = True
    globals.SIGINT_TRIGGERED = True
    #global process_completed
    print("SIGINT received. Stopping background task...")
    while not globals.PROCESS_COMPLETED:
        time.sleep(10)
        print("Waiting for background task to complete...")
      
    sys.exit(0)


signal.signal(signal.SIGINT, handle_sigint)

def main():
    """Run administrative tasks."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "api.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
    

