from rest_framework import serializers
from .models import Landscape

class LandscapeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Landscape
        fields = [  'id',
                    'name',
                    'description',
                    'filename',
                    'image_url',
                    'user_ip_list',
                    'monster_ip_list',
                    'landscape_type',
                    'feature',
                    'monsters',
                    ]
