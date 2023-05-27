from django.db import models
from monster_app.models import Monster

class Battle(models.Model):
    attacker = models.ForeignKey(Monster, on_delete=models.CASCADE, related_name='attacker_monsters')
    defender = models.ForeignKey(Monster, on_delete=models.CASCADE, related_name='defender_monsters')
    winner = models.ForeignKey(Monster, on_delete=models.SET_NULL, related_name='winner_monsters', null=True, blank=True)
    loser = models.ForeignKey(Monster, on_delete=models.SET_NULL, related_name='loser_monsters', null=True, blank=True)
    winner_xp_gain = models.IntegerField(null=True, blank=True)
    loser_xp_gain = models.IntegerField(null=True, blank=True)
    battle_date = models.DateTimeField(auto_now_add=True)
