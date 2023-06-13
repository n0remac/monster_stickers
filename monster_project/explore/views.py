import openai
import random
import json
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.urls import reverse
from .models import Story
from monster_app.models import Monster
from .serializer import StorySerializer
from .adventure_generator import get_location


@api_view(['GET'])
def get_adventure(request, monster_id):
    monster = Monster.objects.get(id=monster_id)
    # create an empty story
    story_obj = Story.objects.create(monster=monster)

    story = run_prompt(get_location())
    story_obj.content = story.get('choices')[0].get('message').get('content')
    
    serializer = StorySerializer(story_obj)

    return Response(serializer.data)

@login_required
def story_detail_view(request, story_id):
    story = get_object_or_404(Story, id=story_id)
    return render(request, 'explore/story_detail.html', {'story': story})

@login_required
def story_list_view(request, monster_id):
    stories = Story.objects.filter(monster_id=monster_id).order_by('-created_at')
    return render(request, 'explore/story_list.html', {'stories': stories, 'monster_id': monster_id, 'num_stories': len(stories)})

@login_required
def generate_story(request, monster_id):
    monster = Monster.objects.get(id=monster_id)
    # create an empty story
    story_obj = Story.objects.create(monster=monster)

    story, conflict_creature = random_story(monster_id)
    complete_story = story['setup'] + story['conflict'] + story['resolution']
    generated_story = run_prompt(complete_story)
    content = generated_story['choices'][0]['message']['content']
    # update story with content
    story_obj.content = content
    story_obj.conflict_creature = conflict_creature
    story_obj.save()

    return HttpResponseRedirect(reverse('story_detail_view', args=(story_obj.id,)))

def run_prompt(prompt):
    story = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=[
            {"role": "system", "content": "You are a seasoned and eloquent storyteller in a fantasy world and you will write a fantasy short story."},
            {"role": "user", "content": prompt},
        ]
    )
    return story


def random_story(monster_id):
    # Load the story archetypes from the JSON file
    with open('story_archetypes.json') as f:
        story_archetypes = json.load(f)

    # Randomly select a story archetype
    story_archetype = random.choice(story_archetypes)

    # Get the monster's details
    try:
        monster = Monster.objects.get(id=monster_id)
    except ObjectDoesNotExist:
        return "Monster does not exist."

    # Randomly select a setting and a conflict creature
    setting = monster.description

    unclaimed_monsters = Monster.objects.filter(owner=None)
    conflict_creature = random.choice(unclaimed_monsters)

    story = {
        'type': story_archetype['type'],
        'setup': story_archetype['setup'].format(creature=monster.creature, element_type=monster.element_type, setting=monster.element_type),
        'conflict': story_archetype['conflict'].format(conflict_creature=conflict_creature.creature, conflict_element=monster.description),
        'resolution': story_archetype['resolution'].format(creature=monster.creature, element_type=monster.element_type, conflict_creature=conflict_creature.creature)
    }

    return story, conflict_creature

