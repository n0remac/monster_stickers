from django.contrib import admin
from .models import UserProfile, UnregisteredUser

admin.site.register(UserProfile)
admin.site.register(UnregisteredUser)