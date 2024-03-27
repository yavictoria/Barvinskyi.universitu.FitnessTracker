from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from .models import Workout, FitnessGoal, CompletedGoals
from .views import register_workout, workout_logs, create_fitness_goal, choose_goal, log_goal_record, completed_goal
from .forms import FitnessGoalForm, FitnessGoalSelectionForm, FitnessRecordForm


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
        self.assertEqual(response.status_code, 200)  # Should return success