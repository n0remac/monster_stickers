import openai
import random
import json
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Story
from monster_app.models import Monster


@login_required
def story_list_view(request, monster_id):
    stories = Story.objects.filter(monster_id=monster_id).order_by('-created_at')
    return render(request, 'explore/story_list.html', {'stories': stories})

@login_required
def generate_story(request, element_type, creature, monster_id):
    monster = Monster.objects.get(id=monster_id)
    story, conflict_creature = random_story(monster_id)

    complete_story = story['setup'] + story['conflict'] + story['resolution']
    generated_story = run_prompt(complete_story)
    new_story = Story.objects.create(
        monster=monster,
        content=generated_story['choices'][0]['message']['content'],
        conflict_creature=conflict_creature
    )

    return render(request, 'explore/story.html', {'story': new_story})

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
    random_monster = random.choice(unclaimed_monsters)

    conflict_creature = random_monster
    print(conflict_creature.creature)

    # Fill in the placeholders in the story archetype
    story = {
        'type': story_archetype['type'],
        'setup': story_archetype['setup'].format(creature=monster.creature, element_type=monster.element_type, setting=monster.element_type),
        'conflict': story_archetype['conflict'].format(conflict_creature=conflict_creature.creature, conflict_element=monster.description),
        'resolution': story_archetype['resolution'].format(creature=monster.creature, element_type=monster.element_type, conflict_creature=conflict_creature.creature)
    }

    return story, conflict_creature

