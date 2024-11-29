import numpy as np
import cards
import players
import utility as util
import history
import bot

ROUND = 1
MODE_AVAILABLE = np.array(['easy', 'normal', 'hard'])
MODE = None
for index, mode in np.ndenumerate(MODE_AVAILABLE):
    print(f"{index[0]+1}. {mode.capitalize()}")
MODE = input("Select mode : ")
MODE = MODE_AVAILABLE[int(MODE)-1]

NUMBER_OR_PLAYERS = input('How many players (dealer not included) : ')
players.set_players(int(NUMBER_OR_PLAYERS),1)
PLAYERS, DEALERS = players.get_players()
print('Players available : ')
for p in PLAYERS: print(p)
PLAYER = input('Choose player to play with : p-')
PLAYER = f"p-{PLAYER}"

players_available = PLAYERS.size
# Loop each round
while 1 < players_available:
    print(players_available)
    print(ROUND)
    for _ in range(2):
        for index, player in np.ndenumerate(PLAYERS):
            if (ROUND > 1 and history.HISTORY[ROUND-1][player] != ['surrender']) or (ROUND == 1):
                players.set_cards(f"{player}", cards.get_shuffled_card(1))
        players.set_cards('d-1', cards.get_shuffled_card(1))

    for index, player in np.ndenumerate(PLAYERS):
        players.set_cards_state(str(player), players.PLAYER_CARDS[player][0], players.PLAYER_CARDS[player][1])
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
    print()
    for index, player in np.ndenumerate(PLAYERS):
        if player == PLAYER:
            print(f"{players.get_player_names(player)} playing. Your turn!")
            player_hand = cards.play_hand()
            history.record(ROUND, player, player_hand)
            if player_hand == 'hit':
                players.set_cards(f"{player}", cards.hit())
            elif player_hand == 'surrender':
                util.end_program('You surrender, game ended')
            print(f"{players.get_player_names(player)} choose {player_hand.upper()}")
        else:
            if (ROUND > 1 and history.HISTORY[ROUND-1][player] != ['surrender']) or (ROUND == 1):
                print(f"{players.get_player_names(player)} is playing ...")
                bot_cards = np.array([players.PLAYER_CARDS[player][0], players.PLAYER_CARDS[player][1]])
                bot_hand = bot.play(MODE, player, bot_cards, players.DEALER_CARDS['d-1'])
                history.record(ROUND, player, bot_hand)
                util.sleep_terminal(1.5)
                util.delete_prevline()
                print(f"{players.get_player_names(player)} choose {bot_hand.upper()}")
    
    players_available = 0
    for index, player in np.ndenumerate(PLAYERS):
        if history.HISTORY[ROUND][player] != ['surrender']:
            players_available += 1
    ROUND += 1
    players.reset()
    cards.reset()
    cards.play()
    util.pause_terminal()