from rest_framework import serializers
from .models import UnregisteredUser

class UnregisteredUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnregisteredUser
        fields = ['ip', 'monsters']