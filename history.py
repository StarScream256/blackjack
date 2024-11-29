HISTORY = {}
WINNING_HISTORY = {}


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

if __name__ == '__main__':
    record(1, 'p-1', 'stand')
    print(HISTORY)
    record(1, 'p-1', 'hit')
    print(HISTORY)
    record(2, 'p-1', 'surrender')
    print(HISTORY)