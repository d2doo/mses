# PROJECT urls.py

from django.contrib import admin
from django.urls import path, include
from .views import social_login_redirect, index

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('users/', include('users.urls')),
    path('accounts/3rdparty/signup/', social_login_redirect),
    path('', index),
]
