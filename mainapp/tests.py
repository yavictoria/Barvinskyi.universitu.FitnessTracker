from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from django.core import mail
from django.test import Client


from .models import Workout, FitnessGoal, CompletedGoals, Badge, Achievement
from .views import register_workout, workout_logs, create_fitness_goal, choose_goal, log_goal_record, completed_goal, \
    update_workout_achievements, update_achievements, award_badge
from mainapp.management.commands.check_workout import Command


class WorkoutViewTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='password')
        self.goal1 = FitnessGoal.objects.create(user=self.user, goal_type='weight_loss', description='Lose weight',
                                                target_value=10)
        self.goal2 = FitnessGoal.objects.create(user=self.user, goal_type='muscle_gain', description='Gain muscle',
                                                target_value=20)

    def test_register_workout_view(self):
        request = self.factory.post('/register-workout/',
                                    {'description': 'Test Workout', 'all_sets_done': True, 'all_arms_done': True,
                                     'all_legs_done': True, 'all_chest_done': True})
        request.user = self.user
        response = register_workout(request)
        self.assertEqual(response.status_code,
                         302)  # Check if redirecting to home after successful workout registration

    def test_workout_logs_view(self):
        # Create sample workout logs
        Workout.objects.create(user=self.user, description='Workout 1', all_sets_done=True, all_arms_done=True,
                               all_legs_done=True, all_chest_done=True)
        Workout.objects.create(user=self.user, description='Workout 2', all_sets_done=True, all_arms_done=False,
                               all_legs_done=True, all_chest_done=False)
        Workout.objects.create(user=self.user, description='Workout 3', all_sets_done=False, all_arms_done=True,
                               all_legs_done=False, all_chest_done=True)

        request = self.factory.get('/dashboard/')
        request.user = self.user
        response = workout_logs(request)

        self.assertEqual(response.status_code, 200)  # Check if response is successful

        # Check if the rendered HTML contains expected elements
        self.assertIn(b'Workout 1', response.content)  # Check for a specific workout description
        self.assertIn(b'Workout 2', response.content)  # Check for another specific workout description
        self.assertIn(b'Workout 3', response.content)  # Check for yet another specific workout description

    def test_create_fitness_goal_view(self):
        request = self.factory.post('/create_fitness_goal/',
                                    {'goal_type': 'endurance_improvement', 'description': 'Improve endurance',
                                     'target_value': 30})
        request.user = self.user
        response = create_fitness_goal(request)
        self.assertEqual(response.status_code, 302)  # Should redirect to profile

    def test_choose_goal_view(self):
        request = self.factory.post('/choose_goal/', {'goal': self.goal1.id})
        request.user = self.user
        response = choose_goal(request)
        self.assertEqual(response.status_code, 302)  # Should redirect to log_goal_record

    def test_log_goal_record_view(self):
        request = self.factory.post('/log_goal_record/{}/'.format(self.goal1.id), {'achieved_value': 12})
        request.user = self.user
        response = log_goal_record(request, self.goal1.id)
        self.assertEqual(response.status_code, 302)  # Should redirect to profile

        # Check if the goal is completed and deleted
        completed_goal = CompletedGoals.objects.filter(goal_type='weight_loss', user=self.user).first()
        self.assertIsNotNone(completed_goal)
        self.assertEqual(completed_goal.target_value, 10)
        self.assertEqual(completed_goal.achieved_value, 12)
        self.assertIsNone(FitnessGoal.objects.filter(id=self.goal1.id).first())

    def test_completed_goal_view(self):
        request = self.factory.get('/completed_goal/')
        request.user = self.user
        response = completed_goal(request)
        self.assertEqual(response.status_code, 200)

    class WorkoutNotificationTestCase(TestCase):
        def setUp(self):
            # Create a test user
            self.user = User.objects.create_user(username='testuser', email='pashchuknik@gmail.com',
                                                 password='testpassword')

            # Create old workouts
            Workout.objects.create(user=self.user, date=timezone.now() - timezone.timedelta(days=10),
                                   description='Test workout 1')
            Workout.objects.create(user=self.user, date=timezone.now() - timezone.timedelta(days=8),
                                   description='Test workout 2')

        def test_send_notifications(self):
            # Call the management command
            command = Command()
            command.handle()

            # Print out the contents of the outbox
            for email in mail.outbox:
                print(f"To: {email.to}, Subject: {email.subject}")

            # Check that one email was sent
            self.assertEqual(len(mail.outbox), 2)

            # Verify email contents
            email = mail.outbox[0]
            self.assertEqual(email.subject, 'Reminder: Last Workout Was More Than a Week Ago')
            self.assertEqual(email.to, ['pashchuknik@gmail.com'])


class AchievementsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')
        self.client = Client()

    def test_achievements_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('achievements'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('workout_badge' in response.context)
        self.assertTrue('goal_badge' in response.context)
        self.assertTrue('post_badge' in response.context)
        self.assertTrue('comments_badge' in response.context)

    def test_award_badge_function(self):
        award_badge(self.user, 'bronze', 'Workout')
        self.assertTrue(Badge.objects.filter(user=self.user, badge_type='bronze', awarded_for='Workout').exists())

    def test_update_workout_achievements_function(self):
        achievements = Achievement.objects.create(user=self.user, workouts_num=5)
        update_workout_achievements(self.user, achievements)
        self.assertTrue(Badge.objects.filter(user=self.user, badge_type='bronze', awarded_for='Workout').exists())

    def test_update_achievements_function(self):
        awarded_for_values = ['Workout', 'Goal', 'Post', 'Comment']
        for awarded_for in awarded_for_values:
            Badge.objects.create(user=self.user, badge_type='bronze', awarded_for=awarded_for)
        update_achievements(self.user)
        for awarded_for in awarded_for_values:
            self.assertTrue(Badge.objects.filter(user=self.user, awarded_for=awarded_for).exists())