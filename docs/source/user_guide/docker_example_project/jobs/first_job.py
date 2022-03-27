from datetime import timedelta

import regta


@regta.thread_job(interval=timedelta(seconds=44))
def first_job():
    """Everything this function returns will be logged. If an exception
    occurs in this function, it will be logged as an error.
    """
    # Put your code here
    return "Hello from first_job! This message is displayed every 44 seconds."
