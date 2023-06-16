from django.db import models
import uuid
from datetime import datetime, timezone
import json

class GameEntity(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    attack = models.IntegerField(default=0)
    health = models.IntegerField(default=0)
    xp = models.IntegerField(default=0)
    max_health = models.IntegerField(default=0)
    max_attack = models.IntegerField(default=0)
    max_xp = models.IntegerField(default=0)
    conscious = models.BooleanField(default=True)
    last_battle = models.DateTimeField(null=True, blank=True)
    location_x = models.IntegerField(default=0)
    location_y = models.IntegerField(default=0)

    def current_health(self):
        if not self.conscious:  # The monster was unconscious
            time_passed = datetime.now(timezone.utc) - self.last_battle
            recovery = (time_passed.total_seconds() / (24 * 60 * 60)) * self.max_health  # recovered health over time
            print(f"Recovery: {recovery}")
            new_health = min(int(recovery), self.max_health)
            if new_health == self.max_health:
                self.conscious = True
            return new_health
        else:  # The monster was conscious
            return self.health

    def save(self, *args, **kwargs):
        self.health = self.current_health()
        super().save(*args, **kwargs)

class Monster(GameEntity):
    element_type = models.CharField(max_length=200, default='')
    creature = models.CharField(max_length=200, default='')
    description = models.TextField(default='')
    owner = models.ForeignKey('auth.User', related_name='monsters', on_delete=models.CASCADE, null=True, blank=True)
    filename = models.CharField(max_length=200, default='', null=True, blank=True)
    ip_list = models.TextField(default='[]')

    def set_ip(self, ip):
        ip_list = self.get_ip_list()
        if ip not in ip_list:
            ip_list.append(ip)
            self.ip_list = json.dumps(ip_list)
            self.save()
    
    def get_ip_list(self):
        return json.loads(self.ip_list)

    def image_url(self):
        if self.filename == '':
            return f"/static/monsterimages/{self.element_type}-{self.creature}.png"
        return f"/static/monsterimages/{self.filename}"
