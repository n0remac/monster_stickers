from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Battle
from monster_app.models import Monster
import random
from datetime import datetime, timezone

@login_required
def attack_view(request, defender_id):
    user_monsters = Monster.objects.filter(owner=request.user)
    defender = Monster.objects.get(id=defender_id)
    
    if request.method == 'POST':
        attacker_id = request.POST.get('monster')
        if str(attacker_id) == str(defender_id):
            return redirect('monster_detail', element_type=defender.element_type, creature=defender.creature, id=defender.id)

        attacker = Monster.objects.get(id=attacker_id)
        if attacker.health <= 0:
            return redirect('monster_detail', element_type=defender.element_type, creature=defender.creature, id=defender.id)
        
        battle = Battle(attacker=attacker, defender=defender)
        battle.save()
        return redirect('battle_view', battle_id=battle.id)
        
    return render(request, 'attack.html', {'user_monsters': user_monsters, 'defender': defender})

@login_required
def battle_view(request, battle_id):
    def end_battle(attacker, defender, winner, loser):
        attacker.last_battle = datetime.now(timezone.utc)
        winner.xp += loser.xp // 2 + loser.max_xp // 2
        loser.xp += winner.max_xp // 4
        loser.conscious = False
        attacker.save()
        defender.last_battle = datetime.now(timezone.utc)
        defender.save()
        battle.winner = winner
        battle.save()
        return redirect('monster_detail', element_type=defender.element_type, creature=defender.creature, id=defender.id)
    
    battle = Battle.objects.get(id=battle_id)
    attacker = battle.attacker
    defender = battle.defender
    result = None

    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'Attack':
            attacker_damage = random.randint(0, attacker.attack)
            defender_damage = random.randint(0, defender.attack)
            
            if attacker_damage > defender.health:
                result = 'You won the battle!'
                defender.health = 0
                return end_battle(attacker, defender, attacker, defender)
            if defender_damage > attacker.health:
                result = 'You lost the battle.'
                attacker.health = 0
                return end_battle(attacker, defender, defender, attacker)
            else:
                attacker.health -= defender_damage
                defender.health -= attacker_damage
                attacker.save()
                defender.save()
        elif action == 'Run':
            return redirect('monster_detail', element_type=defender.element_type, creature=defender.creature, id=defender.id)
        
    return render(request, 'battle.html', {
        'attacker': attacker,
        'defender': defender,
        'result': result,
    })

@login_required
def spend_xp_view(request, monster_id):
    monster = Monster.objects.get(id=monster_id)

    # Ensure the user owns this monster
    if monster.owner != request.user:
        return redirect('monster_app:index')

    if request.method == 'POST':
        spend_option = request.POST.get('spend_option')
        if spend_option == 'health':
            if monster.xp > 0 and monster.current_health() < monster.max_health:
                monster.health += 1
                monster.xp -= 1
        elif spend_option == 'attack':
            if monster.xp >= 100:
                monster.attack += 1
                monster.xp -= 100
        elif spend_option == 'max_health':
            if monster.xp >= 100:
                monster.max_health += 1
                monster.xp -= 100
        monster.save()

    return render(request, 'battle_app/spend_xp.html', {'monster': monster})
