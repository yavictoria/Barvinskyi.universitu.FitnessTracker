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


class FitnessGoal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    goal_type_choices = [
        ('weight_loss', 'Weight Loss'),
        ('muscle_gain', 'Muscle Gain'),
        ('endurance_improvement', 'Endurance Improvement'),
    ]
    goal_type = models.CharField(max_length=100, choices=goal_type_choices)
    description = models.CharField(max_length=200)
    target_value = models.FloatField()
    achieved_value = models.FloatField(default=0)

    def __str__(self):
        return self.description


class CompletedGoals(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    goal_type_choices = [
        ('weight_loss', 'Weight Loss'),
        ('muscle_gain', 'Muscle Gain'),
        ('endurance_improvement', 'Endurance Improvement'),
    ]
    goal_type = models.CharField(max_length=100, choices=goal_type_choices)
    description = models.CharField(max_length=200)
    target_value = models.FloatField()
    achieved_value = models.FloatField(default=0)