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

    def __str__(self):
        return self.description


class Activity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    completed_goal = models.ForeignKey(CompletedGoals, on_delete=models.CASCADE)
    pub_date = models.DateTimeField(default=timezone.now)
    content = models.TextField()
    likes = models.IntegerField(default=0)


class UserLiked(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, related_name='comments')
    comment_text = models.TextField()
    pub_date = models.DateTimeField(default=timezone.now)


class SendNotif(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    accept_notif = models.BooleanField(default=True)


class Achievement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    workouts_num = models.IntegerField(default=0)
    goals_num = models.IntegerField(default=0)
    posts_num = models.IntegerField(default=0)
    comments_num = models.IntegerField(default=0)


class Badge(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    badge_type = models.CharField(max_length=50)
    awarded_for = models.CharField(max_length=50, default='Comment')


class Friendship(models.Model):
    user = models.ForeignKey(User, related_name='friends', on_delete=models.CASCADE)
    friend = models.ForeignKey(User, related_name='user_friends', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'friend']
