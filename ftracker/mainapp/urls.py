from django.urls import path, include
from . import views
from django.views.generic.base import RedirectView


urlpatterns = [
    #path('google/login/', RedirectView.as_view(url='/accounts/google/login/')),
    path("ftracker_registration/", include("allauth.urls")),
    path('accounts/google/login/callback/', views.callback_view, name='google_callback'),
    path('', views.home, name='home'),
    path("", include("allauth.urls")),
]
