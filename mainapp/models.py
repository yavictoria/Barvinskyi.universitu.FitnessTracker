from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Workout(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    description = models.TextField()
    all_sets_done = models.BooleanField(default=False)
    all_arms_done = models.BooleanField(default=False)
    all_legs_done = models.BooleanField(default=False)
    all_chest_done = models.BooleanField(default=False)