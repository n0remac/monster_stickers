from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import Monster
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import MonsterSerializer

@api_view(['POST'])
def create_monster(request):
    serializer = MonsterSerializer(data=request.data)
    if serializer.is_valid():
        monster = serializer.save()
        return Response({'id': monster.id}, status=201)
    return Response(serializer.errors, status=400)

def monster_list(request):
    monsters = Monster.objects.all()
    return render(request, 'monster_list.html', {'monsters': monsters})

def monster_detail(request, element_type, creature, id):
    monster = get_object_or_404(Monster, element_type=element_type, creature=creature, id=id)
    monster.save()
    return render(request, 'monster_detail.html', {'monster': monster})

@login_required
def claim_monster(request, element_type, creature, monster_id):
    # use serializer to update the monster's owner as the current user
    try:
        monster = get_object_or_404(Monster, element_type=element_type, creature=creature, id=monster_id, owner=None)
        monster.owner = request.user
        monster.save()
    except:
        return redirect('monster_detail', element_type=element_type, creature=creature, id=monster_id)
    

    # Redirect the user to some page, such as the monster detail page
    return redirect('monster_detail', element_type=element_type, creature=creature, id=monster_id)
