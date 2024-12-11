from django.shortcuts import render
from allauth.socialaccount.models import SocialAccount

def landing_view(request):
    return render(request, 'landing.html')

def userinfo_view(request):
    social_account = SocialAccount.objects.filter(user=request.user).first()
    extra_data = social_account.extra_data if social_account else {}

    return render(request, 'userinfo.html', {'extra_data': extra_data})
