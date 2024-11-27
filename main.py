import numpy as np
import cards
import players
import utility as util

ROUND = 1
NUMBER_OR_PLAYERS = input('How many players (dealer not included) : ')
players.set_players(int(NUMBER_OR_PLAYERS),1)
PLAYERS, DEALERS = players.get_players()
print('Players available : ')
for p in PLAYERS: print(p)
PLAYER = input('Choose player to play with : p-')
PLAYER = f"p-{PLAYER}"

for _ in range(2):
    for index, player in np.ndenumerate(PLAYERS):
        players.set_cards(f"{player}", cards.get_shuffled_card(1))

for index, player in np.ndenumerate(PLAYERS):
    print(f"{player}{' (you)' if player == PLAYER else ''} - ", end='')
    player_cards = players.PLAYER_CARDS[player]
    for index, _ in enumerate(player_cards):
        first_loop = index == 0
        last_loop = index == len(player_cards) - 1
        print(f"{'' if first_loop else ' '}{players.PLAYER_CARDS[player][index]} {cards.get_card_value(players.PLAYER_CARDS[player][index])}{'' if last_loop else ','}", end='')
    print()

util.pause_terminal()
for index, player in np.ndenumerate(PLAYERS):
    if player == PLAYER:
        print('Choose your hand ...')
        print('1. Stand')
        print('2. Hit')
        print('3. Surrender')
    else:
        pass


    