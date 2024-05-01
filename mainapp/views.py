from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout
from django.conf import settings
from django.core.mail import send_mail
from django.db.models import Count

from .forms import WorkoutForm, FitnessGoalForm, FitnessRecordForm, FitnessGoalSelectionForm, ActivityForm, CommentForm
from .models import Workout, FitnessGoal, CompletedGoals, Activity, UserLiked, SendNotif, Badge, Achievement, Friendship


def award_badge(user, badge_type, awarded_for):
    Badge.objects.create(user=user, badge_type=badge_type, awarded_for=awarded_for)


def update_workout_achievements(user, achievements):
    workout_count = achievements.workouts_num
    if workout_count == 5 and not Badge.objects.filter(user=user, badge_type='bronze', awarded_for='Workout').exists():
        award_badge(user, 'bronze', awarded_for='Workout')
    elif workout_count == 10 and not Badge.objects.filter(user=user, badge_type='silver',
                                                          awarded_for='Workout').exists():
        award_badge(user, 'silver', awarded_for='Workout')
    elif workout_count == 50 and not Badge.objects.filter(user=user, badge_type='gold', awarded_for='Workout').exists():
        award_badge(user, 'gold', awarded_for='Workout')
    elif workout_count == 100 and not Badge.objects.filter(user=user, badge_type='brilliant',
                                                           awarded_for='Workout').exists():
        award_badge(user, 'brilliant', awarded_for='Workout')


def update_goal_achievements(user, achievements):
    goal_count = achievements.goals_num
    if goal_count == 5 and not Badge.objects.filter(user=user, badge_type='bronze', awarded_for='Goal').exists():
        award_badge(user, 'bronze', awarded_for='Goal')
    elif goal_count == 10 and not Badge.objects.filter(user=user, badge_type='silver', awarded_for='Goal').exists():
        award_badge(user, 'silver', awarded_for='Goal')
    elif goal_count == 50 and not Badge.objects.filter(user=user, badge_type='gold', awarded_for='Goal').exists():
        award_badge(user, 'gold', awarded_for='Goal')
    elif goal_count == 100 and not Badge.objects.filter(user=user, badge_type='brilliant', awarded_for='Goal').exists():
        award_badge(user, 'brilliant', awarded_for='Goal')


def update_post_achievements(user, achievements):
    post_count = achievements.posts_num
    if post_count == 5 and not Badge.objects.filter(user=user, badge_type='bronze', awarded_for='Post').exists():
        award_badge(user, 'bronze', awarded_for='Post')
    elif post_count == 10 and not Badge.objects.filter(user=user, badge_type='silver', awarded_for='Post').exists():
        award_badge(user, 'silver', awarded_for='Post')
    elif post_count == 50 and not Badge.objects.filter(user=user, badge_type='gold', awarded_for='Post').exists():
        award_badge(user, 'gold', awarded_for='Post')
    elif post_count == 100 and not Badge.objects.filter(user=user, badge_type='brilliant', awarded_for='Post').exists():
        award_badge(user, 'brilliant', awarded_for='Post')


def update_comment_achievements(user, achievements):
    comment_count = achievements.comments_num
    if comment_count == 5 and not Badge.objects.filter(user=user, badge_type='bronze', awarded_for='Comment').exists():
        award_badge(user, 'bronze', awarded_for='Comment')
    elif comment_count == 10 and not Badge.objects.filter(user=user, badge_type='silver',
                                                          awarded_for='Comment').exists():
        award_badge(user, 'silver', awarded_for='Comment')
    elif comment_count == 50 and not Badge.objects.filter(user=user, badge_type='gold', awarded_for='Comment').exists():
        award_badge(user, 'gold', awarded_for='Comment')
    elif comment_count == 100 and not Badge.objects.filter(user=user, badge_type='brilliant',
                                                           awarded_for='Comment').exists():
        award_badge(user, 'brilliant', awarded_for='Comment')


def update_achievements(user):
    achievements, _ = Achievement.objects.get_or_create(user=user)
    update_workout_achievements(user, achievements)
    update_goal_achievements(user, achievements)
    update_post_achievements(user, achievements)
    update_comment_achievements(user, achievements)
    achievements.save()


def home(request):
    activities = Activity.objects.order_by('-pub_date')[:5]
    comment_form = CommentForm()
    return render(request, "activity_feed.html", {'activities': activities, 'comment_form': comment_form})


def profile(request):
    user = request.user
    completed_goals_count = CompletedGoals.objects.filter(user=user).count()
    activities_count = Activity.objects.filter(user=user).count()
    workouts_count = Workout.objects.filter(user=user).count()
    badges = Badge.objects.filter(user=user).values('badge_type').annotate(count=Count('id'))

    username = None
    if request.user.is_authenticated:
        username = request.user.username

    send_notif, created = SendNotif.objects.get_or_create(user=user)
    if send_notif.accept_notif:
        return render(request, "profile_content.html", {'username': username, 'send_notif': send_notif,
                                                        'completed_goals_count': completed_goals_count,
                                                        'activities_count': activities_count,
                                                        'workouts_count': workouts_count,
                                                        'badges': badges})
    else:
        return render(request, "profile_content.html", {'username': username,
                                                        'completed_goals_count': completed_goals_count,
                                                        'activities_count': activities_count,
                                                        'workouts_count': workouts_count,
                                                        'badges': badges})


def other_profile(request, user_id):
    if user_id == request.user.id:
        return redirect('profile')

    user = User.objects.filter(id=user_id).first()
    completed_goals_count = CompletedGoals.objects.filter(user=user).count()
    activities_count = Activity.objects.filter(user=user).count()
    workouts_count = Workout.objects.filter(user=user).count()
    badges = Badge.objects.filter(user=user).values('badge_type').annotate(count=Count('id'))

    context = {
        'completed_goals_count': completed_goals_count,
        'activities_count': activities_count,
        'workouts_count': workouts_count,
        'badges': badges,
        'username': user.username,
        'user_id':user_id
    }
    return render(request, 'friends_profile.html', context)


def add_friend(request, friend_id):
    friend = User.objects.get(id=friend_id)
    if friend != request.user:
        Friendship.objects.get_or_create(user=request.user, friend=friend)
    return redirect('home')


def friends_list(request):
    friends = Friendship.objects.filter(user=request.user).all()
    return render(request, 'friends_list.html', {'friends': friends})


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
            achievements, _ = Achievement.objects.get_or_create(user=request.user)
            achievements.workouts_num += 1
            achievements.save()
            update_achievements(request.user)
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
    completed_goals = CompletedGoals.objects.filter(user=request.user)[:5]
    return render(request, 'dashboard_summary.html', {
        'logs': logs,
        'percentage_all_sets_done': percentage_all_sets_done,
        'percentage_all_arms_done': percentage_all_arms_done,
        'percentage_all_legs_done': percentage_all_legs_done,
        'percentage_all_chest_done': percentage_all_chest_done,
        'completed_goals': completed_goals,
    })


def create_fitness_goal(request):
    if request.method == 'POST':
        form = FitnessGoalForm(request.POST)
        if form.is_valid():
            fitness_goal = form.save(commit=False)
            fitness_goal.user = request.user
            fitness_goal.save()
            return redirect('profile')
    else:
        form = FitnessGoalForm()
    return render(request, 'set_goal.html', {'form': form})


def choose_goal(request):
    if request.method == 'POST':
        form = FitnessGoalSelectionForm(request.POST)
        if form.is_valid():
            selected_goal_id = form.cleaned_data['goal'].id
            return redirect('log_goal_record', goal_id=selected_goal_id)
    else:
        form = FitnessGoalSelectionForm()
    return render(request, 'select_goal.html', {'form': form})


def log_goal_record(request, goal_id):
    fitness_goal = get_object_or_404(FitnessGoal, id=goal_id, user=request.user)
    if request.method == 'POST':
        form = FitnessRecordForm(request.POST)
        if form.is_valid():
            achieved_value = form.cleaned_data['achieved_value']
            fitness_goal.achieved_value += achieved_value
            if fitness_goal.achieved_value >= fitness_goal.target_value:
                completed_goal = CompletedGoals.objects.create(
                    user=request.user,
                    goal_type=fitness_goal.goal_type,
                    description=fitness_goal.description,
                    target_value=fitness_goal.target_value,
                    achieved_value=fitness_goal.achieved_value
                )
                achievements, _ = Achievement.objects.get_or_create(user=request.user)
                achievements.goals_num += 1
                achievements.save()
                update_achievements(request.user)
                fitness_goal.delete()
                notif_obj, created = SendNotif.objects.get_or_create(user=request.user)
                if notif_obj.accept_notif:
                    user = request.user
                    subject = 'Congratulations!'
                    message = f"{user.username}, you've completed your goal: {fitness_goal.description}. Keep going!"
                    from_email = settings.EMAIL_HOST_USER
                    recipient_list = [user.email]
                    send_mail(subject, message, from_email, recipient_list, fail_silently=False)
                    count = CompletedGoals.objects.count()
                    if count % 5 == 0 and count != 0:
                        subject = 'Congratulations!'
                        message = (
                            f"{user.username}, you've completed your {count}th goal: {fitness_goal.description}. "
                            f"Keep going!")
                        from_email = settings.EMAIL_HOST_USER
                        recipient_list = [user.email]
                        send_mail(subject, message, from_email, recipient_list, fail_silently=False)
                    return redirect('profile')
                return redirect('profile')
            fitness_goal.save()
            return redirect('profile')
    else:
        form = FitnessRecordForm()
    return render(request, 'log_goal.html', {'form': form})


def completed_goal(request):
    return render(request, 'goal_completed.html')


def create_activity(request):
    if request.method == 'POST':
        form = ActivityForm(request.user, request.POST)
        if form.is_valid():
            activity = form.save(commit=False)
            activity.user = request.user
            completed_goal = form.cleaned_data['completed_goal']
            activity.completed_goal = completed_goal
            activity.save()
            achievements, _ = Achievement.objects.get_or_create(user=request.user)
            achievements.posts_num += 1
            achievements.save()
            update_achievements(request.user)
            return redirect('home')  # Redirect to the homepage after creating activity
    else:
        form = ActivityForm(request.user)
    return render(request, 'create_activity.html', {'form': form})


def add_comment(request, activity_id):
    activity = Activity.objects.get(pk=activity_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.activity = activity
            comment.save()
            achievements, _ = Achievement.objects.get_or_create(user=request.user)
            achievements.comments_num += 1
            achievements.save()
            update_achievements(request.user)
            return redirect('home')
    else:
        form = CommentForm()
    return render(request, 'homepage.html', {'form': form})


def like_activity(request, activity_id):
    if request.method == 'POST':
        activity = get_object_or_404(Activity, pk=activity_id)
        user_liked = UserLiked.objects.filter(user=request.user, activity=activity)
        if user_liked.exists():
            user_liked.delete()
            activity.likes -= 1
            activity.save()
        else:
            UserLiked.objects.create(user=request.user, activity=activity)
            activity.likes += 1
            activity.save()
        return redirect('home')


def toggle_notification_setting(request):
    if request.method == 'POST':
        user = request.user
        if SendNotif.objects.filter(user=user).exists():
            send_notif = SendNotif.objects.get(user=user)
            send_notif.accept_notif = not send_notif.accept_notif
            send_notif.save()
            return redirect('profile')
        else:
            send_notif = SendNotif.objects.create(user=user, accept_notif=False)
            return redirect('profile')

    else:
        send_notif = SendNotif.objects.filter(user=request.user).first()
        return redirect('profile')


def achievements(request):
    workout_badge = Badge.objects.filter(user=request.user, awarded_for='Workout').values('badge_type').annotate(
        count=Count('badge_type'))
    goal_badge = Badge.objects.filter(user=request.user, awarded_for='Goal').values('badge_type').annotate(
        count=Count('badge_type'))
    post_badge = Badge.objects.filter(user=request.user, awarded_for='Post').values('badge_type').annotate(
        count=Count('badge_type'))
    comments_badge = Badge.objects.filter(user=request.user, awarded_for='Comment').values('badge_type').annotate(
        count=Count('badge_type'))

    return render(request, 'achievements.html',
                  {'workout_badge': workout_badge, 'goal_badge': goal_badge, 'post_badge': post_badge,
                   'comments_badge': comments_badge})