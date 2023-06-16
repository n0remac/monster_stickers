from django.db import models
from monster_app.models import Monster

class Story(models.Model):
    monster = models.ForeignKey(Monster, on_delete=models.CASCADE, related_name='initial_monster')
    content = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    conflict_creature = models.ForeignKey(Monster, on_delete=models.CASCADE, related_name='conflict_monster', null=True)

class Adventure(models.Model):
    monster = models.ForeignKey(Monster, on_delete=models.CASCADE, related_name='adventure_monster')
    content = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    location_x = models.IntegerField(default=0)
    location_y = models.IntegerField(default=0)