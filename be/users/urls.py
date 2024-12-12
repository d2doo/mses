from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import landing_view, userinfo_view, signup_view, login_view

urlpatterns = [
    path('landing/', landing_view, name='landing'),
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('userinfo/', userinfo_view, name='userinfo'),
    path('logout/', LogoutView.as_view(), name='logout'),
]