from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.conf import settings
from django.core.mail import send_mail


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
