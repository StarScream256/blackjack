import numpy as np
import cards
import players
import utility as util
import history
import bot

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
    players.set_cards('d-1', cards.get_shuffled_card(1))

for index, player in np.ndenumerate(PLAYERS):
    print(f"{players.get_player_names(player)}{' (you)' if player == PLAYER else ''} - ", end='')
    player_cards = players.PLAYER_CARDS[player]
    for index, _ in enumerate(player_cards):
        first_loop = index == 0
        last_loop = index == len(player_cards) - 1
        print(f"{'' if first_loop else ' '}{players.PLAYER_CARDS[player][index]} {cards.get_card_value(players.PLAYER_CARDS[player][index])}{'' if last_loop else ','}", end='')
    print()
for index, dealer in np.ndenumerate(DEALERS):
    print(f"{players.get_dealer_names(dealer)} (dealer) - ", end='')
    dealer_cards = players.DEALER_CARDS[dealer]
    for index, _ in enumerate(dealer_cards):
        first_loop = index == 0
        last_loop = index == len(dealer_cards) - 1
        if last_loop:
            print(f"{'' if first_loop else ' '}{players.DEALER_CARDS[dealer][index]} {cards.get_card_value(players.DEALER_CARDS[dealer][index])}{'' if last_loop else ', '}", end='')
        else:
            print('[secret],', end='')
    print()

util.pause_terminal()
for index, player in np.ndenumerate(PLAYERS):
    if player == PLAYER:
        player_hand = cards.play_hand()
        history.record(ROUND, player, player_hand)
        if player_hand == 'hit':
            players.set_cards(f"{player}", cards.hit())
        elif player_hand == 'surrender':
            util.end_program('You surrender, game ended')
    else:
        pass


    