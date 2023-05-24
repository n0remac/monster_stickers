from django.urls import path
from . import views

urlpatterns = [
    path('accounts/profile/', views.profile, name='profile'),
    path('accounts/register/', views.register, name='register'),
]
