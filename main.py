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

def show_player_cards():
    for index, player in np.ndenumerate(PLAYERS):
        if players.PLAYER_CARDS[player] != {}:
            players.set_cards_state(str(player), players.PLAYER_CARDS[player][0], players.PLAYER_CARDS[player][1])
            print(f"{players.get_player_names(player)}{' (you)' if player == PLAYER else ''} - ", end='')
            player_cards = players.PLAYER_CARDS[player]
            for index, _ in enumerate(player_cards):
                first_loop = index == 0
                last_loop = index == len(player_cards) - 1
                print(f"{'' if first_loop else ' '}{players.PLAYER_CARDS[player][index]} {cards.get_card_value(players.PLAYER_CARDS[player][index])}{'' if last_loop else ','}", end='')
            print()

def show_dealer_cards(is_begin: bool, total_val: int):
    for index, dealer in np.ndenumerate(DEALERS):
        print(f"{players.get_dealer_names(dealer)} (dealer) - ", end='')
        dealer_cards = players.DEALER_CARDS[dealer]
        for index, _ in enumerate(dealer_cards):
            first_loop = index == 0
            last_loop = index == len(dealer_cards) - 1
            if is_begin:
                if last_loop :
                    print(f"{'' if first_loop else ' '}{players.DEALER_CARDS[dealer][index]} {cards.get_card_value(players.DEALER_CARDS[dealer][index])}{'' if last_loop else ', '}", end='')
                else:
                    print('[secret],', end='')
            else:
                print(f"{'' if first_loop else ' '}{players.DEALER_CARDS[dealer][index]} {cards.get_card_value(players.DEALER_CARDS[dealer][index])}{'' if last_loop else ', '}", end='')
        print(f"\nDealer total value : {total_val}") if is_begin == False else ''
        print()


players_available = PLAYERS.size
while 1 < players_available:
    print(players_available)
    print(ROUND)
    for _ in range(2):
        for index, player in np.ndenumerate(PLAYERS):
            if (ROUND > 1 and history.HISTORY[ROUND-1][player] != ['surrender']) or (ROUND == 1):
                players.set_cards(str(player), cards.get_shuffled_card(1))
        players.set_cards('d-1', cards.get_shuffled_card(1))
    
    dealer_card1_val = (bot.decide_ace_value(cards.get_card_value(players.DEALER_CARDS[DEALERS[0]][1])[0], True if players.DEALER_CARDS[DEALERS[0]][1].endswith('ace') else False) if players.DEALER_CARDS[DEALERS[0]][0].endswith('ace') else cards.get_card_value(players.DEALER_CARDS[DEALERS[0]][0])[0])
    dealer_card2_val = (bot.decide_ace_value(cards.get_card_value(players.DEALER_CARDS[DEALERS[0]][0])[0], True if players.DEALER_CARDS[DEALERS[0]][0].endswith('ace') else False) if players.DEALER_CARDS[DEALERS[0]][1].endswith('ace') else cards.get_card_value(players.DEALER_CARDS[DEALERS[0]][1])[0])
    dealer_card_val = dealer_card1_val + dealer_card2_val

    show_player_cards()
    show_dealer_cards(True, dealer_card_val)

    util.pause_terminal()
    print()
    for index, player in np.ndenumerate(PLAYERS):
        if player == PLAYER:
            print(f"{players.get_player_names(player)} playing. Your turn!")
            player_cards_val = 0
            player_cards = players.PLAYER_CARDS[str(player)]
            player_hand = cards.play_hand()
            if player_hand.startswith('stand'):
                if player_hand == 'stand_22_ace':
                    player_cards_val = 22
                elif player_hand == 'stand_12_ace':
                    player_cards_val = 12
                elif player_hand == 'stand_make_ace_11':
                    for index, (key, value) in enumerate(player_cards):
                        if player_cards[key].endswith('ace'):
                            player_cards_val += 11
                        else:
                            player_cards_val += cards.get_card_value(player_cards[key])[0]
                elif player_hand == 'stand_make_ace_1':
                    for index, (key, value) in enumerate(player_cards):
                        if player_cards[key].endswith('ace'):
                            player_cards_val += 1
                        else:
                            player_cards_val += cards.get_card_value(player_cards[key])[0]
                elif player_hand == 'stand':
                    for index, (key, value) in enumerate(player_cards):
                        player_cards_val += cards.get_card_value(player_cards[key])[0]
                player_hand = 'stand'
            elif player_hand == 'hit':
                players.set_cards(str(player), cards.hit())
                player_cards = players.PLAYER_CARDS[str(player)]
                for index, (key, value) in enumerate(player_cards):
                    if player_cards[key].endswith('ace'):
                        for index, (key, value) in enumerate(player_cards):
                            if not player_cards[key].endswith('ace'):
                                player_cards_val += cards.get_card_value(player_cards[key])[0]
                        player_cards_val += bot.decide_ace_value(player_cards_val, False)
                    else:
                        player_cards_val += cards.get_card_value(player_cards[key])[0]
            elif player_hand == 'surrender':
                util.end_program('You surrender, game ended')
            
            history.record(ROUND, str(player), player_hand)
            history.win_record(ROUND, str(player), cards.evaluate_hand(player_cards_val, dealer_card_val))
            print(f"{players.get_player_names(player)} (you) choose {player_hand.upper()}")
        else:
            if (ROUND > 1 and history.HISTORY[ROUND-1][player] != ['surrender']) or (ROUND == 1):
                print(f"{players.get_player_names(player)} is playing ...")
                bot_cards = np.array([players.PLAYER_CARDS[player][0], players.PLAYER_CARDS[player][1]])
                bot_cards_val = 0
                bot_hand = bot.play(MODE, player, bot_cards, players.DEALER_CARDS['d-1'])

                if bot_hand == 'hit': players.set_cards(str(player), cards.hit())
                bot_cards = np.array([players.PLAYER_CARDS[player][0], players.PLAYER_CARDS[player][1], players.PLAYER_CARDS[player][2]])
                for index, card in np.ndenumerate(bot_cards):
                    if card.endswith('ace'):
                        for index, card in np.ndenumerate(bot_cards):
                            if not card.endswith('ace'):
                                bot_cards_val += cards.get_card_value(card)[0]
                        bot_cards_val += bot.decide_ace_value(bot_cards_val, False)
                    else:
                        bot_cards_val += cards.get_card_value(card)[0]
                
                history.record(ROUND, player, bot_hand)

                # next : add history winning record

                util.sleep_terminal(1.5)
                util.delete_prevline()
                if players.PLAYER_CARDS[player] != {}:
                    print(f"{players.get_player_names(player)} choose {bot_hand.upper()}")
            elif ROUND > 1 and history.HISTORY[ROUND-1][player] == ['surrender']:
                history.record(ROUND, player, 'surrender')

        print(history.WINNING_HISTORY)
    show_dealer_cards(is_begin=False, total_val=dealer_card_val)

    # next : show whow won

    players_available = 0
    print(history.HISTORY)
    for index, player in np.ndenumerate(PLAYERS):
        if history.HISTORY[ROUND][player] != ['surrender']:
            players_available += 1
    ROUND += 1
    players.reset()
    cards.reset()
    cards.play()
    util.pause_terminal()