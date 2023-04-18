from celery import shared_task
from time import sleep

@shared_task
def spleepy(duration):
    sleep(duration)
    print("oi")
    return None

@shared_task
def verifyTimeToSelect():
    global startTimeToSelect
    print("StartTimeToSelect: ", startTimeToSelect.strftime("%H:%M:%S"))
    return None 