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
    dealer_upcard_val = cards.get_card_value(dealer_upcard)[0]
    if player_card_state == 'hard':
        for card in np.nditer(player_cards):
            card = str(card)
            player_card_value += cards.get_card_value(card)[0]
        consider = hard_total(player_card_value, dealer_upcard_val)
    elif player_card_state == 'soft':
        card_type = np.array(['h', 'c', 's', 'd'])
        ace_index = 0
        for index, card in np.ndenumerate(player_cards):
            if 'ace' in str(card): ace_index = index
        print(type(ace_index))
        player_cards = np.delete(player_cards, ace_index[0])
        for card in np.nditer(player_cards):
            card = str(card)
            player_card_value += cards.get_card_value(card)[0]
        consider = soft_total(player_card_value, dealer_upcard_val)
    elif player_card_state == 'same':
        card1_ace = player_cards[0].endswith('ace')
        card2_ace = player_cards[1].endswith('ace')
        if card1_ace and card2_ace:
            for card in np.nditer(player_cards):
                player_card_value += decide_ace_value(player_card_value, True)
            consider = hard_total(player_card_value, dealer_upcard_val)
        elif card1_ace or card2_ace:
            if card1_ace:
                card2_val = cards.get_card_value(player_cards[1])[0]
                card1_val = decide_ace_value(card2_val, False)
                consider = hard_total(card1_val+card2_val, dealer_upcard_val)
            if card2_ace:
                card1_val = cards.get_card_value(player_cards[0])[0]
                card2_val = decide_ace_value(card1_val, False)
                consider = hard_total(card1_val+card2_val, dealer_upcard_val)
        else:
            player_cards_value = cards.get_card_value(player_cards[0])[0] + cards.get_card_value(player_cards[1])[0]
            consider = hard_total(player_cards_value, dealer_upcard_val)
    return consider


def play(mode: str, player: str, cards: np.ndarray, dealer_upcard: str):
    bot_hand = ''
    if mode == 'easy':
        bot_hand = random_select()
    elif mode == 'normal':
        randomize = np.random.randint(0, 1)
        if randomize == 0: bot_hand = random_select()
        else: bot_hand = probability_select(player, cards, str(dealer_upcard))
    elif mode == 'hard':
        bot_hand = probability_select(player, cards, str(dealer_upcard))
    return bot_hand
    
if __name__ == '__main__':
   print(probability_select('p-1', np.array(['s-5', 'h-ace']), 'h-10'))