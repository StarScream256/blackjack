import numpy as np

card_type = np.array(['ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'king', 'queen', 'jack'])
hearts = np.array([])
diamonds = np.array([])
clubs = np.array([])
spades = np.array([])
cards = np.array([])

SESSION_SHUFFLED = np.array([])
CARDS_OUT = np.array([])

for c in card_type:
    hearts = np.append(hearts, f"h-{c}")
    diamonds = np.append(diamonds, f"d-{c}")
    clubs = np.append(clubs, f"c-{c}")
    spades = np.append(spades, f"s-{c}")
cards = np.concatenate((hearts, diamonds, clubs, spades))

def _get_cards(presented: np.ndarray) -> np.ndarray:
    filtered = []
    for c in cards:
        if np.where(presented == c)[0].size != 0:
            filtered.append(False)
        else:
            filtered.append(True)
    return cards[filtered]

def _shuffle(presented: np.ndarray) -> np.ndarray:
    remaining_cards = _get_cards(presented)
    shuffled_cards = np.full_like(remaining_cards, "", dtype=object)
    for index in range(remaining_cards.size):
        while True:
            random = np.random.randint(0, remaining_cards.size)
            raised_index = np.where(remaining_cards == remaining_cards[random])[0]
            if np.where(shuffled_cards == remaining_cards[raised_index])[0].size == 0:
                shuffled_cards[[index]] = remaining_cards[raised_index]
                break
    return shuffled_cards

def get_shuffled_card(returned: int) -> np.ndarray:
    global CARDS_OUT
    result = np.array([])
    for _ in range(returned):
        global SESSION_SHUFFLED
        result = np.append(result, SESSION_SHUFFLED[-1])
        CARDS_OUT = np.append(CARDS_OUT, SESSION_SHUFFLED[-1])
        SESSION_SHUFFLED = np.delete(SESSION_SHUFFLED, [-1])
    return result

def get_card_value(card: str) -> list[int]:
    checked = card.split('-')[1]
    if checked == "ace":
        return [1,11]
    elif checked.isnumeric():
        return [int(checked)]
    else:
        return [10]

def hit():
    global SESSION_SHUFFLED
    result = np.array([])
    result = np.append(result, SESSION_SHUFFLED[-1])
    CARDS_OUT = np.append(CARDS_OUT, SESSION_SHUFFLED[-1])
    SESSION_SHUFFLED = np.delete(SESSION_SHUFFLED, [-1])
    return result

def play():
    global SESSION_SHUFFLED
    SESSION_SHUFFLED = _shuffle(np.array([]))

play()