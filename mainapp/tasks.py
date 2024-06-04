from celery import shared_task
from django.core.management import call_command


@shared_task
def check_workout_schedule():
    call_command('check_workout')