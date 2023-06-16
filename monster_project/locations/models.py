from django.db import models
import uuid
import json
from monster_app.models import Monster

class Landscape(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    description = models.TextField()
    filename = models.CharField(max_length=200, default='', null=True, blank=True)
    landscape_type = models.CharField(max_length=200, default='')
    feature = models.CharField(max_length=200, default='')
    user_ip_list = models.TextField(default='[]')
    monster_ip_list = models.TextField(default='[]')
    monsters = models.ManyToManyField(Monster, blank=True)

    def set_user_ip(self, user_ip):
        user_ip_list = self.get_user_ip_list()
        if user_ip not in user_ip_list:
            user_ip_list.append(user_ip)
            self.user_ip_list = json.dumps(user_ip_list)
            self.save()
    
    def get_user_ip_list(self):
        return json.loads(self.user_ip_list)
    
    def set_monster_ip(self, monster_ip):
        monster_ip_list = self.get_monster_ip_list()
        if monster_ip not in monster_ip_list:
            monster_ip_list.append(monster_ip)
            self.monster_ip_list = json.dumps(monster_ip_list)
            self.save()
    
    def get_monster_ip_list(self):
        return json.loads(self.monster_ip_list)

    def __str__(self):
        return self.name

    def image_url(self):
        return f"/static/locationimages/{self.filename}"