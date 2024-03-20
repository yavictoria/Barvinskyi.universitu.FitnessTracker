from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from .models import Workout
from .views import register_workout, workout_logs


class WorkoutViewTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='password')

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