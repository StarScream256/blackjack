HISTORY = {}

def record(round: int, player: str, hand: str):
    if round not in HISTORY:
        HISTORY[round] = {}
    if player not in HISTORY[round]:
        HISTORY[round][f"{player}"] = []
    HISTORY[round][player].append(hand.lower())

if __name__ == '__main__':
    record(1, 'p-1', 'stand')
    print(HISTORY)
    record(1, 'p-1', 'hit')
    print(HISTORY)
    record(2, 'p-1', 'surrender')
    print(HISTORY)