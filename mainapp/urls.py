from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path("accounts/", include("allauth.urls")),
    path('profile/', views.profile, name='profile'),
    path('logout/', views.logout_view, name='logout_view'),
    path('profile/register_workout/', views.register_workout, name='register_workout'),
    path('profile/set_goal', views.create_fitness_goal, name='create_fitness_goal'),
    path('profile/choose_goal', views.choose_goal, name='choose_goal'),
    path('profile/complete_goal', views.completed_goal, name='completed_goal'),
    path('profile/log_goal/<int:goal_id>/', views.log_goal_record, name='log_goal_record'),
    path('dashboard/', views.workout_logs, name='workout_logs'),
    path('create_activity/', views.create_activity, name='create_activity'),
    path('add_comment/<int:activity_id>', views.add_comment, name='add_comment'),
    path('like/<int:activity_id>/', views.like_activity, name='like_activity'),
]