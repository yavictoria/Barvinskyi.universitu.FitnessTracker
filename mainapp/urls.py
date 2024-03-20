from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path("accounts/", include("allauth.urls")),
    path('profile/', views.profile, name='profile'),
    path('logout/', views.logout_view, name='logout_view'),
    path('profile/register_workout/', views.register_workout, name='register_workout'),
    path('dashboard/', views.workout_logs, name='workout_logs'),
]