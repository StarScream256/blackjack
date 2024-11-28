import numpy as np
import cards
import history
import players

def random_select() -> str:
    choices = [0, 1, 2]
    probabilities = [0.5, 0.3, 0.2]
    random = np.random.choice(choices, p=probabilities)
    return cards.HAND_CHOICES[random]

def decide_ace_value(curval: int, pair_ace: bool) -> int:
    decide = ''
    if pair_ace:
        if curval == 0: decide = 11
        else: decide = 1
    else:
        as_one_cond = (curval > 10)
        as_eleven_cond = (curval <= 10)
        if as_one_cond: decide = 1
        elif as_eleven_cond: decide = 11
    return decide
    
def hard_total(pcv: int, dcv: int) -> str:
    consider = ''
    stand_condition = (18 <= pcv <= 21 and 2 <= dcv <= 11) or (13 <= pcv  <= 17 and 2 <= dcv <= 6)or (pcv == 12 and 4 <= dcv <= 6) or (pcv == 17 and 7 <= dcv <= 11)
    hit_condition = (3 <= pcv <= 16 and 7 <= dcv <= 11) or (3 <= pcv <= 11 and 2 <= dcv <= 6) or (pcv == 12 and 2 <= dcv <= 3)
    if stand_condition: consider = 'stand'
    elif hit_condition: consider = 'hit'
    else: consider = 'surrender'
    return consider

def soft_total(pair: int, dcv: int) -> str:
    '''
    Bot hand consideration on soft total card value

    Args:
        pair (int): The value of the pair of ace card.
        dcv (int): The value of dealer upcard.

    Returns:
        str: The hand consideration
    '''
    consider = ''
    stand_condition = (7 <= pair <= 9 and 2 <= dcv <= 8) or (8 <= pair <= 9 and 9 <= dcv <= 11)
    hit_condition = (2 <= pair <= 6 and 2 <= dcv <= 11) or (pair == 7 and 9 <= dcv <= 11)
    if stand_condition: consider = 'stand'
    elif hit_condition: consider = 'hit'
    else: consider = 'surrender'
    return consider

def probability_select(player: str, player_cards: np.ndarray, dealer_upcard: str) -> str:
    consider = ''
    player_card_value = 0
    player_card_state = players.PLAYER_CARDS_STATE[player]
    if player_card_state == 'hard':
        for card in np.nditer(player_cards):
            player_card_value += cards.get_card_value(card)
        consider = hard_total(player_card_value, cards.get_card_value(dealer_upcard))
    elif player_card_state == 'soft':
        card_type = np.array(['h', 'c', 's', 'd'])
        ace_index = np.where([card + '-ace' in player_cards for card in card_type])
        player_cards = np.delete(player_cards, ace_index)
        for card in np.nditer(player_cards):
            player_card_value += cards.get_card_value(card)
        consider = soft_total(player_card_value, cards.get_card_value(dealer_upcard))
    elif player_card_state == 'same':
        if player_cards[0].endswith('ace') and player_cards[1].endswith('ace'):
            for card in np.nditer(player_cards):
                player_card_value += decide_ace_value(player_card_value, True)
            consider = hard_total(player_card_value, cards.get_card_value(dealer_upcard))
        elif player_cards[0].endswith('ace') or player_cards[1].endswith('ace'):
            pass

def play(player: str, cards: np.ndarray):
    pass

if __name__ == '__main__':
   print(soft_total(7,10))