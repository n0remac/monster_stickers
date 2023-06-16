from rest_framework import serializers
from .models import Story, Adventure

class StorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Story
        fields = ['monster',
                'content',
                'created_at',
                'conflict_creature',
        ]

class AdventureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Adventure
        fields = ['monster',
                'content',
                'created_at',
                'location_x',
                'location_y',
        ]