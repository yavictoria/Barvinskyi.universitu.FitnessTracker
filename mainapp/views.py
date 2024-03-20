from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.conf import settings
from django.core.mail import send_mail
from .forms import WorkoutForm
from .models import Workout


# Create your views here.
def home(request):
    return render(request, "homepage.html")


def profile(request):
    username = None
    if request.user.is_authenticated:
        username = request.user.username
    return render(request, "profile.html", {'username': username})


def logout_view(request):
    logout(request)
    return redirect("home")


@login_required
def welcome_email(request):
    user = request.user
    subject = 'Welcome to Fitness Tracker!'
    message = f'{user.username}, thanks for becoming a part of our gym community!'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [user.email]
    send_mail(subject, message, from_email, recipient_list, fail_silently=False)
    return redirect('home')


def register_workout(request):
    if request.method == 'POST':
        form = WorkoutForm(request.POST)
        if form.is_valid():
            workout = form.save(commit=False)
            workout.user = request.user
            workout.save()
            return redirect('home')
    else:
        form = WorkoutForm()
    return render(request, 'register_workout.html', {'form': form})


def workout_logs(request):
    total_logs = Workout.objects.filter(user=request.user).order_by('-date').all()

    total_workouts = total_logs.count()
    total_all_sets_done = total_logs.filter(all_sets_done=True).count()
    total_all_arms_done = total_logs.filter(all_arms_done=True).count()
    total_all_legs_done = total_logs.filter(all_legs_done=True).count()
    total_all_chest_done = total_logs.filter(all_chest_done=True).count()

    # Calculate percentages
    percentage_all_sets_done = (total_all_sets_done / total_workouts) * 100 if total_workouts > 0 else 0
    percentage_all_arms_done = (total_all_arms_done / total_workouts) * 100 if total_workouts > 0 else 0
    percentage_all_legs_done = (total_all_legs_done / total_workouts) * 100 if total_workouts > 0 else 0
    percentage_all_chest_done = (total_all_chest_done / total_workouts) * 100 if total_workouts > 0 else 0

    logs = Workout.objects.filter(user=request.user).order_by('-date')[:5]
    return render(request, 'dashboard_summary.html', {
        'logs': logs,
        'percentage_all_sets_done': percentage_all_sets_done,
        'percentage_all_arms_done': percentage_all_arms_done,
        'percentage_all_legs_done': percentage_all_legs_done,
        'percentage_all_chest_done': percentage_all_chest_done,
    })