import random
from collections import Counter

class CardDef:
    def __init__(self, name, attribute=None, ctype=None, level=None, atk=None, deff=None, category='monster'):
        self.name = name
        self.attribute = attribute
        self.ctype = ctype
        self.level = level
        self.atk = atk
        self.deff = deff
        self.category = category
    def is_monster(self):
        return self.category == 'monster'

deck_template = []
def add_copies(name, n, attribute=None, ctype=None, level=None, atk=None, deff=None, category='monster'):
    for _ in range(n):
        deck_template.append(CardDef(name, attribute, ctype, level, atk, deff, category))

# ===================== Decklist =========================

#  MUST SPECIFY ALL FIELDS FOR MONSTERS 
#  For spells/traps, just specify name and category='st' 

# ========================================================

add_copies('Razen', 3, 'Fire', 'Warrior', 4, 1800, 1500)
add_copies('Jiaolong', 3, 'Fire', 'Wyrm', 5, 2400, 2100)
add_copies('Ash Blossom', 3, 'Fire', 'Zombie', 3, 0, 1800)
add_copies('Dogoran', 1, 'Fire', 'Dragon', 8, 3000, 1200)
add_copies('Borger', 2, 'Dark', 'Machine', 7, 2500, 1500)
add_copies('Madlove', 3, 'Dark', 'Fiend', 4, 1200, 2000)
add_copies('Magnamhut', 1, 'Dark', 'Dragon', 6, 2500, 2000)
add_copies('Shifter', 1, 'Dark', 'Spellcaster', 6, 1200, 2200)
add_copies('Jokull', 2, 'Dark', 'Aqua', 5, 2000, 1900)
add_copies('Phantazmay', 2, 'Dark', 'Dragon', 7, 2400, 1800)
add_copies('Holy Sue', 3, 'Earth', 'Psychic', 5, 500, 22000)
add_copies('Valius', 1, 'Earth', 'Dragon', 8, 3000, 1500)
add_copies('Izuna', 3, 'Earth', 'Warrior', 5, 2100, 1600)
add_copies('Lupus', 1, 'Earth', 'Beast-Warrior', 5, 2300, 200)
add_copies('Fuwalos', 3, 'Wind', 'Winged Beast', 4, 100, 600)
add_copies('AttrSS', 3, category='st')
add_copies('AddRazen', 1, category='st')
add_copies('MultiTutor', 1, category='st')
add_copies('Excavate6', 1, category='st')
add_copies('GenericST', 2, category='st')

# ==== Card Number = 40, can change when needed ====
assert len(deck_template) == 40

def count_name(hand, name):
    return sum(1 for c in hand if c.name == name)
def attrs_counts(hand):
    return Counter(c.attribute for c in hand if c.is_monster())
def has_attr(hand, attr):
    return any(c.is_monster() and c.attribute == attr for c in hand)

# ==== Check if exactly one attribute among level, attribute, type, atk, deff matches ====
def exactly_one_match(a, b):
    matches = 0
    matches += int(a.attribute == b.attribute)
    matches += int(a.level == b.level)
    matches += int(a.ctype == b.ctype)
    matches += int(a.atk == b.atk)
    matches += int(a.deff == b.deff)
    return matches == 1

# ==== Base conditions for combos ====
def razen_base(hand):
    if count_name(hand, 'Razen') >= 1:
        a = attrs_counts(hand)
        if a.get('Fire',0) >= 2 or a.get('Dark',0) >= 1:
            return True
    return False

def madlove_base(hand):
    if count_name(hand, 'Madlove') >= 1 and attrs_counts(hand).get('Fire',0) >= 1:
        return True
    return False

def holysue_base(hand):
    a = attrs_counts(hand)
    if count_name(hand, 'Holy Sue') >= 1 and a.get('Fire',0) >= 1 and a.get('Dark',0) >= 1:
        return True
    return False

# ==== Enabling conditions ====
def can_attrss_enable(hand, rem, target):
    if not any(c.name=='AttrSS' for c in hand):
        return False
    if target=='Razen':
        need_attr = 'Fire'
    elif target=='Madlove':
        need_attr = 'Dark'
    else:
        need_attr = 'Earth'
    if not has_attr(hand, need_attr):
        return False
    return any(c.name==target for c in rem)

def can_addrazen_enable(hand, rem):
    if not any(c.name=='AddRazen' for c in hand):
        return False
    a = attrs_counts(hand)
    if (a.get('Fire',0) >= 1 or a.get('Dark',0) >= 1) and any(c.name=='Razen' for c in rem):
        return True
    return False

# Check if MultiTutor can enable the combo for target
def can_multitutor_enable(hand, rem, target_name):
    if not any(c.name=='MultiTutor' for c in hand):
        return False
    if not any(c.is_monster() for c in hand):
        return False
    if not any(c.name==target_name for c in rem):
        return False
    hand_monsters = [c for c in hand if c.is_monster()]
    deck_monsters = [c for c in rem if c.is_monster()]
    targets = [c for c in rem if c.name==target_name]
    for M in hand_monsters:
        for D in deck_monsters:
            if exactly_one_match(M,D):
                for T in targets:
                    if exactly_one_match(D,T):
                        return True
    return False

# Check if adding card_to_add from rem to hand enables the combo for target
def combo_enabled_after_adding(target, hand, rem, card_to_add):
    new_hand = hand + [card_to_add]
    new_rem = [c for c in rem if c is not card_to_add]
    if target=='Razen':
        if razen_base(new_hand): return True
        if can_attrss_enable(new_hand,new_rem,'Razen'): return True
        if can_addrazen_enable(new_hand,new_rem): return True
        if can_multitutor_enable(new_hand,new_rem,'Razen'): return True
        return False
    elif target=='Madlove':
        if madlove_base(new_hand): return True
        if can_attrss_enable(new_hand,new_rem,'Madlove'): return True
        if can_multitutor_enable(new_hand,new_rem,'Madlove'): return True
        return False
    else:
        if holysue_base(new_hand): return True
        if can_attrss_enable(new_hand,new_rem,'Holy Sue'): return True
        if can_multitutor_enable(new_hand,new_rem,'Holy Sue'): return True
        return False

#==== Evaluate hand ====
def evaluate_hand_exact(hand, deck):
    rem = [c for c in deck if c not in hand]
    res = {}
    res['base_R'] = razen_base(hand)
    res['base_M'] = madlove_base(hand)
    res['base_H'] = holysue_base(hand)
    res['attrss_R'] = (not res['base_R']) and can_attrss_enable(hand,rem,'Razen')
    res['attrss_M'] = (not res['base_M']) and can_attrss_enable(hand,rem,'Madlove')
    res['attrss_H'] = (not res['base_H']) and can_attrss_enable(hand,rem,'Holy Sue')
    res['addrazen'] = (not res['base_R']) and (not res['attrss_R']) and can_addrazen_enable(hand,rem)
    res['mt_R'] = (not res['base_R']) and (not res['attrss_R']) and (not res['addrazen']) and can_multitutor_enable(hand,rem,'Razen')
    res['mt_M'] = (not res['base_M']) and (not res['attrss_M']) and can_multitutor_enable(hand,rem,'Madlove')
    res['mt_H'] = (not res['base_H']) and (not res['attrss_H']) and can_multitutor_enable(hand,rem,'Holy Sue')
    def exc_prob(target, already_enabled_flag):
        if already_enabled_flag: return 0.0
        if not any(c.name=='Excavate6' for c in hand): return 0.0
        TRIALS = 40
        hits = 0
        for _ in range(TRIALS):
            sample6 = random.sample(rem, min(6,len(rem)))
            ok = any(combo_enabled_after_adding(target, hand, rem, card) for card in sample6)
            if ok: hits += 1
        return hits/TRIALS
    res['exc_R'] = exc_prob('Razen', res['base_R'] or res['attrss_R'] or res['addrazen'] or res['mt_R'])
    res['exc_M'] = exc_prob('Madlove', res['base_M'] or res['attrss_M'] or res['mt_M'])
    res['exc_H'] = exc_prob('Holy Sue', res['base_H'] or res['attrss_H'] or res['mt_H'])
    pR = 1.0 if (res['base_R'] or res['attrss_R'] or res['addrazen'] or res['mt_R']) else res['exc_R']
    pM = 1.0 if (res['base_M'] or res['attrss_M'] or res['mt_M']) else res['exc_M']
    pH = 1.0 if (res['base_H'] or res['attrss_H'] or res['mt_H']) else res['exc_H']
    res['pR'] = pR
    res['pM'] = pM
    res['pH'] = pH
    p_at_least_one = 1 - (1-pR)*(1-pM)*(1-pH)
    res['p_none'] = 1 - p_at_least_one
    return res

def main():
    TRIALS = 50000
    countR = countM = countH = count_none = 0.0
    for _ in range(TRIALS):
        deck = deck_template[:]
        hand = random.sample(deck,5)
        ev = evaluate_hand_exact(hand, deck)
        countR += ev['pR']
        countM += ev['pM']
        countH += ev['pH']
        count_none += ev['p_none']
    print('Trials:', TRIALS)
    print('Razen ≈', round((countR/TRIALS)*100, 2), '%')
    print('Madlove ≈', round((countM/TRIALS)*100, 2), '%')
    print('Holy Sue ≈', round((countH/TRIALS)*100, 2), '%')
    print('Nessuna combo ≈', round((count_none/TRIALS)*100, 2), '%')


if __name__ == '__main__':
    main()
