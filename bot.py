import numpy as np
import cards
import history
import players

def random_select() -> str:
    choices = [0, 1, 2]
    probabilities = [0.5, 0.3, 0.2]
    random = np.random.choice(choices, p=probabilities)
    return cards.HAND_CHOICES[random]
    
def hard_total(pcv: int, dcv: int) -> str:
    consider = ''
    stand_condition = (18 <= pcv <= 21 and 2 <= dcv <= 11) or (13 <= pcv  <= 17 and 2 <= dcv <= 6)or (pcv == 12 and 4 <= dcv <= 6) or (pcv == 17 and 7 <= dcv <= 11)
    hit_condition = (3 <= pcv <= 16 and 7 <= dcv <= 11) or (3 <= pcv <= 11 and 2 <= dcv <= 6) or (pcv == 12 and 2 <= dcv <= 3)
    if stand_condition: consider = 'stand'
    elif hit_condition: consider = 'hit'
    else: consider = 'surrender'
    return consider

def soft_total(ace_pair: int, dcv: int) -> str:
    consider = ''
    stand_condition = (7 <= ace_pair <= 9 and 2 <= dcv <= 8) or (8 <= ace_pair <= 9 and 9 <= dcv <= 11)
    hit_condition = (2 <= ace_pair <= 6 and 2 <= dcv <= 11) or (ace_pair == 7 and 9 <= dcv <= 11)
    if stand_condition: consider = 'stand'
    elif hit_condition: consider = 'hit'
    else: consider = 'surrender'
    return consider

def same_pair(pair_card: int, dcv: int) -> str:
    consider = ''
    return consider

def probability_select(cards: np.ndarray) -> str:
    pass

def play(player: str, cards: np.ndarray):
    pass

if __name__ == '__main__':
    play('p-1')