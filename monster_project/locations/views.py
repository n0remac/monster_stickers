from typing import Any
from rest_framework import generics
from .models import Landscape
from .serializers import LandscapeSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from utils.utils import get_client_ip
from django.shortcuts import get_object_or_404
from monster_app.models import Monster

class LandscapeDetail(generics.RetrieveUpdateAPIView):
    queryset = Landscape.objects.all()
    serializer_class = LandscapeSerializer

    def get(self, request, *args, **kwargs):
        user_ip = get_client_ip(request)
        Landscape.objects.filter(id=kwargs['pk']).first().set_user_ip(user_ip)
        serliazer = LandscapeSerializer(Landscape.objects.filter(id=kwargs['pk']).first())
        return Response(serliazer.data)


@api_view(['POST'])
def create_landscape(request):
    serializer = LandscapeSerializer(data=request.data)
    if serializer.is_valid():
        landscape = serializer.save()
        return Response({'id': landscape.id}, status=201)
    return Response(serializer.errors, status=400)

@api_view(['POST'])
def add_monster_to_landscape(request):
    landscape = Landscape.objects.get(id=request.data['landscape_id'])
    monster_id = request.data['monster_id']
    monster = get_object_or_404(Monster, id=monster_id)
    landscape.monsters.add(monster)
    landscape.save()
    return Response(status=201)

@api_view(['POST'])
def take_monster_from_landscape(request):
    landscape = Landscape.objects.get(id=request.data['landscape_id'])
    monster_id = request.data['monster_id']
    monster = get_object_or_404(Monster, id=monster_id)
    landscape.monsters.remove(monster)
    landscape.save()
    return Response(status=201)
