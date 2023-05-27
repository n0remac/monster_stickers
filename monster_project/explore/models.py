from django.db import models
from monster_app.models import Monster

class Story(models.Model):
    monster = models.ForeignKey(Monster, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
