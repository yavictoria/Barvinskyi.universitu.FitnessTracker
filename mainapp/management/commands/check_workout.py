from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.core.mail import send_mail
from mainapp.models import Workout


class Command(BaseCommand):
    help = 'Checks workouts and sends notifications if last workout was more than a week ago'

    def handle(self, *args, **options):
        one_week_ago = timezone.now() - timezone.timedelta(days=7)
        old_workouts = Workout.objects.filter(date__lt=one_week_ago)

        for workout in old_workouts:
            subject = 'Reminder: Last Workout Was More Than a Week Ago'
            message = (f"Hi {workout.user.username}, your last workout was on {workout.date}. Please consider "
                       f"scheduling a new one.")
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [workout.user.email]
            send_mail(subject, message, from_email, recipient_list, fail_silently=False)

        self.stdout.write(self.style.SUCCESS('Notifications sent successfully.'))