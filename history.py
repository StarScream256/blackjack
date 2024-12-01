HISTORY = {}
WINNING_HISTORY = {}
VALUE_HISTORY = {}


def record(round: int, player: str, hand: str):
    global HISTORY
    if round not in HISTORY:
        HISTORY[round] = {}
    if player not in HISTORY[round]:
        HISTORY[round][f"{player}"] = []
    HISTORY[round][player].append(hand.lower())

def win_record(round: int, player: str, is_win: bool):
    global WINNING_HISTORY
    if round not in WINNING_HISTORY:
        WINNING_HISTORY[round] = {}
    if player not in WINNING_HISTORY[round]:
        WINNING_HISTORY[round][f"{player}"] = []
    WINNING_HISTORY[round][player].append(is_win)

def value_record(round: int, player: str, cards_val: int):
    global VALUE_HISTORY
    if round not in VALUE_HISTORY:
        VALUE_HISTORY[round] = {}
    if player not in VALUE_HISTORY[round]:
        VALUE_HISTORY[round][f"{player}"] = []
    VALUE_HISTORY[round][player].append(cards_val)

if __name__ == '__main__':
    record(1, 'p-1', 'stand')
    print(HISTORY)
    record(1, 'p-1', 'hit')
    print(HISTORY)
    record(2, 'p-1', 'surrender')
    print(HISTORY)