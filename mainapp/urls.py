from django.urls import path, include
from . import views
from django.views.generic.base import RedirectView


urlpatterns = [
    path('', views.home, name='home'),
    path("accounts/", include("allauth.urls")),
    path('profile/', views.profile, name='profile'),
    path('logout/', views.logout_view, name='logout_view'),
    path('welcome-email/', views.welcome_email, name='welcome_email'),
]
