from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

def social_login_redirect(request):
    return redirect('/users/userinfo')

def index(request):
    if request.user.is_authenticated:
        return redirect('/users/userinfo')
    else:
        return redirect('/users/landing')