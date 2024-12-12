from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, get_backends
from django.contrib.auth.forms import AuthenticationForm
from allauth.socialaccount.models import SocialAccount
from .forms import SignupForm


def landing_view(request):
    if request.user.is_authenticated:
        return redirect('/users/userinfo')
    
    return render(request, 'landing.html')

def userinfo_view(request):
    if not request.user.is_authenticated:
        return redirect('/users/landing')
    
    social_account = SocialAccount.objects.filter(user=request.user).first()
    extra_data = social_account.extra_data if social_account else {}
    context = {
        'extra_data': extra_data
    }
    return render(request, 'userinfo.html', context)


def login_view(request):
    if request.user.is_authenticated:
        return redirect('/users/userinfo/')

    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('/users/userinfo/')
    else:
        form = AuthenticationForm()
    context = {
        'form': form
    }
    return render(request, 'login.html', context)



def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            backend = get_backends()[0]
            auth_login(request, user, backend=backend.__module__ + '.' + backend.__class__.__name__)
            return redirect('/users/userinfo/')
    else:
        form = SignupForm()
    context = {
        'form': form
    }
    return render(request, 'signup.html', context)

