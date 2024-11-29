import numpy as np
import cards

PLAYERS = np.array([])
DEALERS = np.array([])
PLAYER_CARDS = {}
PLAYER_CARDS_STATE = {}
DEALER_CARDS = {}
PLAYER_CARDS_STATE = {}

def set_players(players: int, dealers=1):
    global PLAYERS, DEALERS, PLAYER_CARDS, DEALER_CARDS
    for i in range(players):
        PLAYERS = np.append(PLAYERS, f"p-{i+1}")
        PLAYER_CARDS[f"p-{i+1}"] = {}
    for i in range(dealers):
        DEALERS = np.append(DEALERS, f"d-{i+1}")
        DEALER_CARDS[f"d-{i+1}"] = {}
    
def get_players() -> tuple[np.ndarray, np.ndarray]:
    global PLAYERS, DEALERS
    return PLAYERS, DEALERS

def get_player_names(name: str) -> str:
    if name.startswith('p-'):
        try:
            number = int(name[2:])
            return f"Player {number}"
        except ValueError:
            return "Invalid player"
    else: return "Invalid input prefix"

def get_dealer_names(name: str) -> str:
    if name.startswith('d-'):
        try:
            number = int(name[2:])
            return f"Dealer {number}"
        except ValueError:
            return "Invalid dealer"
    else: return "Invalid input prefix"

def _check_player(player: str) -> bool:
    global PLAYERS
    if np.where(PLAYERS == player)[0].size != 0:
        return True
    else :
        return False

def _check_dealer(dealer: str) -> bool:
    global DEALERS
    if np.where(DEALERS == dealer)[0].size != 0:
        return True
    else :
        return False

def set_cards(player: str, card: str):
    global PLAYER_CARDS, DEALER_CARDS
    if _check_player(player):
        latest_player_card_index = len(PLAYER_CARDS[player])
        PLAYER_CARDS[player][latest_player_card_index] = f"{card[0]}"
    elif _check_dealer(player):
        latest_dealer_card_index = len(DEALER_CARDS[player])
        DEALER_CARDS[player][latest_dealer_card_index] = f"{card[0]}"

def set_cards_state(player: str, card1: str, card2: str):
    global PLAYER_CARDS_STATE, DEALER_CARDS_STATE
    if _check_player(player):
        card1_val = cards.get_card_value(card1)
        card2_val = cards.get_card_value(card2)
        if len(card1_val) == 2 or len(card2_val) == 2:
            PLAYER_CARDS_STATE[player] = 'soft'
        elif len(card1_val) == 1 or len(card1_val) == 1:
            if card1 == card2:
                PLAYER_CARDS_STATE[player] = 'same'
            else:
                PLAYER_CARDS_STATE[player] = 'hard'
    elif _check_dealer(player):
        card1_val = cards.get_card_value(card1)
        card2_val = cards.get_card_value(card2)
        if len(card1_val) == 2 or len(card2_val) == 2:
            DEALER_CARDS_STATE[player] = 'soft'
        elif len(card1_val) == 1 or len(card1_val) == 1:
            if card1 == card2:
                DEALER_CARDS_STATE[player] = 'same'
            else:
                DEALER_CARDS_STATE[player] = 'hard'

def reset():
    global PLAYER_CARDS, PLAYER_CARDS_STATE, DEALER_CARDS, DEALER_CARDS_STATE
    for pc in PLAYER_CARDS:
        PLAYER_CARDS[pc] = {}
    PLAYER_CARDS_STATE = {}
    for dc in DEALER_CARDS:
        DEALER_CARDS[dc] = {}
    PLAYER_CARDS_STATE = {}


if __name__ == '__main__':
    set_players(5,1)
    # set_cards("p-1", np.array(['s-2']))
    # set_cards("p-1", np.array(['s-3']))
    # print(PLAYER_CARDS)
    set_cards_state('p-1', 'h-ace', 's-4')
    set_cards_state('p-2', 'h-3', 's-4')
    print(PLAYER_CARDS_STATE)