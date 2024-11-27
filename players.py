import numpy as np

PLAYERS = np.array([])
DEALERS = np.array([])
PLAYER_CARDS = {}

def set_players(players: int, dealers=1):
    global PLAYERS, DEALERS
    for i in range(players):
        PLAYERS = np.append(PLAYERS, f"p-{i+1}")
        PLAYER_CARDS[f"p-{i+1}"] = {}
    for i in range(dealers):
        DEALERS = np.append(DEALERS, f"d-{i+1}")
    
def get_players() -> tuple[np.ndarray, np.ndarray]:
    global PLAYERS, DEALERS
    return PLAYERS, DEALERS

def _check_player(player: str) -> bool:
    global PLAYERS
    if np.where(PLAYERS == player)[0].size != 0:
        return True
    else :
        return False

def set_cards(player: str, card: str):
    global PLAYER_CARDS
    if _check_player(player):
        latest_index_cards = len(PLAYER_CARDS[player])
        PLAYER_CARDS[player][latest_index_cards] = f"{card[0]}"


if __name__ == '__main__':
    set_players(5,1)
    set_cards("p-1", np.array(['s-2']))
    set_cards("p-1", np.array(['s-3']))
    print(PLAYER_CARDS)