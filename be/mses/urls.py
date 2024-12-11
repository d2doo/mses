# PROJECT urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')), #allauth url
    path('users/', include('users.urls')), # users app url
    # path('', ), # users app url
]
