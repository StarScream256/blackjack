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
while 1 <= players_available:
    util.clear_terminal()
    print(f"Round : {ROUND} - Player : {players_available} - Mode : {MODE.upper()}")
    for _ in range(2):
        for index, player in np.ndenumerate(PLAYERS):
            if (ROUND > 1 and (history.HISTORY[ROUND-1][player] != ['surrender'] and history.WINNING_HISTORY[ROUND-1][player] == [True])) or (ROUND == 1):
                players.set_cards(str(player), cards.get_shuffled_card(1))
        players.set_cards('d-1', cards.get_shuffled_card(1))
    
    dealer_card1_val = (bot.decide_ace_value(cards.get_card_value(players.DEALER_CARDS[DEALERS[0]][1])[0], True if players.DEALER_CARDS[DEALERS[0]][1].endswith('ace') else False) if players.DEALER_CARDS[DEALERS[0]][0].endswith('ace') else cards.get_card_value(players.DEALER_CARDS[DEALERS[0]][0])[0])
    dealer_card2_val = (bot.decide_ace_value(cards.get_card_value(players.DEALER_CARDS[DEALERS[0]][0])[0], True if players.DEALER_CARDS[DEALERS[0]][0].endswith('ace') else False) if players.DEALER_CARDS[DEALERS[0]][1].endswith('ace') else cards.get_card_value(players.DEALER_CARDS[DEALERS[0]][1])[0])
    dealer_cards_val = dealer_card1_val + dealer_card2_val

    show_player_cards()
    show_dealer_cards(True, dealer_cards_val)

    util.pause_terminal()
    print()
    for index, player in np.ndenumerate(PLAYERS):
        if player == PLAYER:
            print(f"{players.get_player_names(player)} playing. Your turn!")
            player_cards_val = 0
            player_cards = players.PLAYER_CARDS[str(player)]
            player_hand = cards.play_hand(player_cards)

            if player_hand.startswith('stand'):
                if player_hand == 'stand_22_ace':
                    player_cards_val = 22
                elif player_hand == 'stand_12_ace':
                    player_cards_val = 12
                elif player_hand == 'stand_make_ace_11':
                    for index, _ in enumerate(player_cards):
                        if player_cards[index].endswith('ace'):
                            player_cards_val += 11
                        else:
                            player_cards_val += cards.get_card_value(player_cards[index])[0]
                elif player_hand == 'stand_make_ace_1':
                    for index, _ in enumerate(player_cards):
                        if player_cards[index].endswith('ace'):
                            player_cards_val += 1
                        else:
                            player_cards_val += cards.get_card_value(player_cards[index])[0]
                elif player_hand == 'stand':
                    for index, _ in enumerate(player_cards):
                        player_cards_val += cards.get_card_value(player_cards[index])[0]
                player_hand = 'stand'
            elif player_hand == 'hit':
                players.set_cards(str(player), cards.hit())
                player_cards = players.PLAYER_CARDS[str(player)]
                for index, _ in enumerate(player_cards):
                    if player_cards[index].endswith('ace'):
                        for index, _ in enumerate(player_cards):
                            if not player_cards[index].endswith('ace'):
                                player_cards_val += cards.get_card_value(player_cards[index])[0]
                        player_cards_val += bot.decide_ace_value(player_cards_val, False)
                    else:
                        player_cards_val += cards.get_card_value(player_cards[index])[0]
            elif player_hand == 'surrender':
                util.end_program('You surrender, game ended')
            
            history.record(ROUND, str(player), player_hand)
            history.win_record(ROUND, str(player), cards.evaluate_hand(player_cards_val, dealer_cards_val))
            history.value_record(ROUND, str(player), player_cards_val)

            print(f"{players.get_player_names(player)} (you) choose {player_hand.upper()}")
        else:
            if (ROUND > 1 and (history.HISTORY[ROUND-1][player] != ['surrender'] and history.WINNING_HISTORY[ROUND-1][player] == [True])) or (ROUND == 1):
                print(f"{players.get_player_names(player)} is playing ...")
                bot_cards = np.array([players.PLAYER_CARDS[player][0], players.PLAYER_CARDS[player][1]])
                bot_cards_val = 0
                bot_hand = bot.play(MODE, player, bot_cards, players.DEALER_CARDS['d-1'])

                if bot_hand == 'hit':
                    players.set_cards(str(player), cards.hit())
                    bot_cards = np.array([players.PLAYER_CARDS[player][0], players.PLAYER_CARDS[player][1], players.PLAYER_CARDS[player][2]])
                
                for index, card in np.ndenumerate(bot_cards):
                    if card.endswith('ace'):
                        for index, card in np.ndenumerate(bot_cards):
                            if not card.endswith('ace'):
                                bot_cards_val += cards.get_card_value(card)[0]
                        bot_cards_val += bot.decide_ace_value(bot_cards_val, False)
                    else:
                        bot_cards_val += cards.get_card_value(card)[0]
                
                history.record(ROUND, str(player), bot_hand)
                history.win_record(ROUND, str(player), cards.evaluate_hand(bot_cards_val, dealer_cards_val))
                history.value_record(ROUND, str(player), bot_cards_val)
            
                util.sleep_terminal(1.5)
                util.delete_prevline()
                if players.PLAYER_CARDS[player] != {}:
                    print(f"{players.get_player_names(player)} choose {bot_hand.upper()}")
            elif ROUND > 1 and ((history.HISTORY[ROUND-1][player] == ['surrender'] and history.WINNING_HISTORY[ROUND-1][player] == [True]) or (history.WINNING_HISTORY[ROUND-1][player] == [False])):
                history.record(ROUND, player, 'surrender')
                history.win_record(ROUND, str(player), False)
                history.value_record(ROUND, str(player), 0)

    show_dealer_cards(is_begin=False, total_val=dealer_cards_val)

    util.debug(history.WINNING_HISTORY)

    players_available = 0
    for index, player in np.ndenumerate(PLAYERS):
        is_win = history.WINNING_HISTORY[ROUND][str(player)][0]
        player_name = players.get_player_names(player)
        player_cards_val = history.VALUE_HISTORY[ROUND][str(player)][0]

        if (ROUND > 1 and history.WINNING_HISTORY[ROUND-1][str(player)][0]) or (ROUND == 1):
            print(f"{player_name}{' (you)' if player == PLAYER else ''} {'WINS' if is_win else 'LOSES'} [{player_cards_val}]")

        if history.HISTORY[ROUND][player] != ['surrender'] and history.WINNING_HISTORY[ROUND][player] == [True]:
            players_available += 1
    
    # next : add termination if player is last man and win onr by one against dealer
    
    ROUND += 1

    players.reset()
    cards.reset()
    cards.play()
    util.pause_terminal()

    is_player_win = history.WINNING_HISTORY[ROUND-1][str(PLAYER)][0]
    if not is_player_win:
        print("\nYou have lost, the game is over")
        util.end_program()