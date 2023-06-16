from django.contrib.auth.models import User
from django.db import models
from monster_app.models import Monster

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class UnregisteredUser(models.Model):
    ip = models.CharField(max_length=200, default='')
    monsters = models.ManyToManyField(Monster)