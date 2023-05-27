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
        defender.last_battle = datetime.now(timezone.utc)

        xp_gain = loser.xp // 2 + loser.max_xp // 2
        winner.xp += xp_gain
        battle.winner_xp_gain = xp_gain
        xp_gain = winner.max_xp // 4
        loser.xp += xp_gain
        battle.loser_xp_gain = xp_gain
        loser.conscious = False

        attacker.save()
        defender.save()
        battle.winner = winner
        battle.loser = loser
        battle.save()
        return redirect('battle_result', battle_id=battle_id)

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
def battle_result_view(request, battle_id):
    battle = Battle.objects.get(id=battle_id)

    if not battle.winner:
        return redirect('monster_app:index')  # Redirect if the battle doesn't have a winner yet

    context = {
        'battle': battle,
        'winner': battle.winner,
        'loser': battle.loser,
        'winner_xp_gain': battle.winner_xp_gain,
        'loser_xp_gain': battle.loser_xp_gain,
    }

    return render(request, 'battle_app/battle_result.html', context)


@login_required
def spend_xp_view(request, monster_id):
    monster = Monster.objects.get(id=monster_id)
    error_message = None

    # Ensure the user owns this monster
    if monster.owner != request.user:
        return redirect('monster_app:index')

    if request.method == 'POST':
        spend_health = int(request.POST.get('spend_health', 0))
        spend_attack = int(request.POST.get('spend_attack', 0)) * 100
        spend_max_health = int(request.POST.get('spend_max_health', 0)) * 100

        total_xp = spend_health + spend_attack + spend_max_health

        if total_xp > monster.xp:
            error_message = "You don't have enough XP for this transaction."
        else:
            if monster.current_health() + spend_health > monster.max_health:
                error_message = "You cannot exceed the maximum health."
            else:
                monster.xp -= total_xp
                monster.health += spend_health
                monster.attack += spend_attack // 100
                monster.max_health += spend_max_health // 100
                monster.save()

    return render(request, 'battle_app/spend_xp.html', {'monster': monster, 'error_message': error_message})


    return render(request, 'battle_app/spend_xp.html', {'monster': monster})
