#!/usr/bin/env python3

from collections import namedtuple
from itertools import starmap
from operator import mul

Action = namedtuple('Action', ['name', 'cost', 'damage', 'heal', 'effect'])
Effect = namedtuple('Effect', ['duration', 'damage', 'armor', 'mana', 'health'])
Player = namedtuple('Player', ['health', 'damage', 'armor', 'mana'])
Boss = namedtuple('Boss', ['health', 'damage', 'armor', 'mana'])

null_effect = Effect(*[0]*5)

action = lambda n, c, d, h, s: Action(n, c, d, h, Effect(*s))

actions = list(starmap(action, [
    ('Magic Missile', 53, 4, 0, null_effect),
    ('Drain', 73, 2, 2, null_effect),
    ('Shield', 113, 0, 0, (6, 0, 7, 0, 0)),
    ('Poison', 173, 0, 0, (6, 3, 0, 0, 0)),
    ('Recharge', 229, 0, 0, (5, 0, 0, 101, 0)),
]))

def can_cast(player, action, schedule=[null_effect]):
    if player.mana < action.cost:
        return False
    # the effect must not be active (multiply as vectors, there should always
    # be a zero on either side)
    if any(starmap(mul, zip(action.effect[1:], schedule[0][1:]))):
        return False
    return True

def cast(player, boss, action, schedule=[]):
    schedule = schedule[:]
    effect = action.effect

    boss = boss._replace(**{'health': boss.health - action.damage})
    player = player._replace(**{
        'mana': player.mana - action.cost,
        'health': player.health + action.heal
    })

    for i in range(effect.duration):
        if len(schedule) <= i:
            schedule.append(null_effect)
        e = schedule[i]
        schedule[i] = e._replace(**{a: getattr(e, a) or getattr(effect, a) for a in e._fields if a != 'duration'})

    return player, boss, schedule

def apply(player, boss, effect):
    boss = boss._replace(**{'health': boss.health - effect.damage})
    player = player._replace(**{
        'armor': effect.armor,
        'mana': player.mana + effect.mana,
        'health': player.health + effect.health
    })
    return player, boss

def explore(player, boss, active, schedule=[null_effect], difficulty=0, cost=0, limit=0):
    #print(player, boss, active, cost, limit, schedule[0])
    effect, *schedule = schedule
    schedule = schedule or [null_effect]
    if active and difficulty:
        player = player._replace(**{'health': player.health - difficulty})
        if player.health <= 0:
            return 0
    player, boss = apply(player, boss, effect)
    if boss.health <= 0:
        #if cost == 900: import ipdb; ipdb.set_trace()
        return cost
    if not active:
        damage = max(1, boss.damage - player.armor)
        health = player.health - damage
        if health <= 0:
            return 0
        player = player._replace(**{'health': health})
        return explore(player, boss, not active, schedule, difficulty=difficulty, cost=cost, limit=limit)
    else:
        mylimit = 0
        for a in actions:
            #print("Trying", a.name, end=' ')
            if not can_cast(player, a, schedule):
                #print("(can't cast)")
                continue
            # prune
            if limit and cost + a.cost > limit:
                #print("(too costly)")
                continue
            #print("")
            player_now, boss_now, schedule_now = cast(player, boss, a, schedule)
            r = explore(player_now, boss_now, not active, schedule_now, difficulty=difficulty, cost=cost + a.cost, limit=limit)
            limit = min(limit, r) or limit or r
            mylimit = min(mylimit, r) or mylimit or r
        return mylimit

player = Player(50, 0, 0, 500)
boss = Boss(51, 9, 0, 0)

print('Easy:', explore(player, boss, True))
print('Hard:', explore(player, boss, True, difficulty=1))
