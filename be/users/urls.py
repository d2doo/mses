from django.urls import path
from .views import landing_view, userinfo_view

urlpatterns = [
    path('landing/', landing_view, name='landing'),
    path('userinfo/', userinfo_view, name='userinfo'),
]