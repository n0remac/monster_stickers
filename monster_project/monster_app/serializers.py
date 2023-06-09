from rest_framework import serializers
from .models import Monster

class MonsterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Monster
        fields = ['id',
                  'element_type',
                  'creature', 
                  'description',
                  'attack',
                  'health',
                  'xp',
                  'conscious',
                  'max_health',
                  'max_attack',
                  'max_xp',
                  'filename',
                  'image_url',]
