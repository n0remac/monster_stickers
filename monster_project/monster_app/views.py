from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from background_task import background
from .models import Monster
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import MonsterSerializer
from explore.models import Story
import openai
from django.http import HttpResponse
from .monster_creation.monster_generator import monster_generator
from django.contrib.auth.models import User
import uuid
from users.models import UnregisteredUser
from users.serializer import UnregisteredUserSerializer
from utils.utils import get_client_ip


@login_required
def perform_breed(request, monster1_id, monster2_id):
    print("Performing breed...")
    generate_monster(request.user.id, str(monster1_id), str(monster2_id))
    return render(request, 'breed_complete.html', {})

@background(schedule=1)
def generate_monster(user_id, monster1_id, monster2_id):
    monster1_id = uuid.UUID(monster1_id)
    monster2_id = uuid.UUID(monster2_id)
    # Retrieve the monsters from the database
    monster1 = get_object_or_404(Monster, id=monster1_id)
    monster2 = get_object_or_404(Monster, id=monster2_id)
    
    user = get_object_or_404(User, id=user_id)
    monster_ids = monster_generator(parent1=monster1, parent2=monster2)
    for monster_id in monster_ids:
        monster = get_object_or_404(Monster, id=monster_id)
        monster.owner = user
        monster.save()

@login_required
def breed_monster(request, monster_id):
    owned_monsters = Monster.objects.filter(owner=request.user).exclude(id=monster_id)
    return render(request, 'breed_monster.html', {'owned_monsters': owned_monsters, 'selected_monster': Monster.objects.get(id=monster_id)})

@api_view(['POST'])
def breed(request):
    user_ip = get_client_ip(request)
    monster1 = get_object_or_404(Monster, id=request.data['monster1_id'])
    monster2 = get_object_or_404(Monster, id=request.data['monster2_id'])
    monster_ids = monster_generator(parent1=monster1, parent2=monster2)
    user = UnregisteredUser.objects.get(ip=user_ip)
    print(monster_ids)
    for monster_id in monster_ids:
        monster = get_object_or_404(Monster, id=monster_id)
        monster.set_ip(user_ip)
        user.monsters.add(monster)
        monster.save()
    return Response({'monster_ids': monster_ids}, status=200)

@api_view(['POST'])
def create_monster(request):
    serializer = MonsterSerializer(data=request.data)
    if serializer.is_valid():
        monster = serializer.save()
        return Response({'id': monster.id}, status=201)
    return Response(serializer.errors, status=400)

@api_view(['POST'])
def get_monster_by_id(request):
    monster = Monster.objects.get(id=request.data['id'])
    serializer = MonsterSerializer(monster)
    return Response(serializer.data)

@api_view(['GET'])
def get_monsters(request):
    monsters = Monster.objects.all()
    serializer = MonsterSerializer(monsters, many=True)
    return Response(serializer.data)

def check_registered_users(user_ip):
    unregistered_user = UnregisteredUser.objects.filter(ip=user_ip)
    if len(unregistered_user) == 0:
        UnregisteredUser.objects.create(ip=user_ip)
    return UnregisteredUser.objects.get(ip=user_ip)

@api_view(['GET'])
def get_monster(request, id):
    user_ip = get_client_ip(request)
    unregistered_user = check_registered_users(user_ip)

    monster = get_object_or_404(Monster, id=id)
    monster.set_ip(user_ip)
    unregistered_user.monsters.add(monster)
    unregistered_user.save()

    serializer = MonsterSerializer(monster)
    return Response(serializer.data)

@api_view(['GET'])
def release_monster(request, id):
    monster = get_object_or_404(Monster, id=id)
    monster.owner = None
    user_id = get_client_ip(request)
    unregistered_user = get_object_or_404(UnregisteredUser, id=user_id)
    unregistered_user.monsters.remove(monster)
    unregistered_user.save()
    monster.save()
    return Response({'id': id}, status=200)

@api_view(['GET'])
def user_monsters(request):
    user_ip = get_client_ip(request)
    check_registered_users(user_ip)
    unregistered_user = get_object_or_404(UnregisteredUser, ip=user_ip)
    serializer = UnregisteredUserSerializer(unregistered_user)
    return Response(serializer.data)

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

@login_required
def generate_story(request, element_type, creature, monster_id):
    monster = Monster.objects.get(id=monster_id)

    # Ensure the user owns this monster
    if monster.owner != request.user:
        return redirect('monster_app:index')

    prompt = f"A {monster.element_type} monster named {monster.creature} embarks on an adventure. {monster.description}. "

    story = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=[
            {"role": "system", "content": "You are a highly intelligent AI and you will write a story."},
            {"role": "user", "content": prompt},
        ]
    )
    
    new_story = Story.objects.create(monster=monster, content=story['choices'][0]['message']['content'])
    new_story.save()

    return render(request, 'explore/story.html', {'story': new_story})