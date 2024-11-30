import numpy as np

card_type = np.array(['ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'king', 'queen', 'jack'])
hearts = np.array([])
diamonds = np.array([])
clubs = np.array([])
spades = np.array([])
cards = np.array([])

SESSION_SHUFFLED = np.array([])
CARDS_OUT = np.array([])

HAND_CHOICES = np.array(['stand_22_ace', 'stand_11_ace', 'stand_make_ace_11', 'stand_make_ace1', 'stand', 'hit', 'surrender'])

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

def play_hand(cards: dict):
    global HAND_CHOICES
    ace_count = np.array([])
    is_have_ace = False
    for key in cards:
        if cards[key].endswith('ace'):
            is_have_ace = True
            ace_count = np.append(ace_count, key)
    if is_have_ace:
        if ace_count.size == 2:
            print("1. Stand with 22")
            print("2. Stand with 12")
        elif ace_count.size == 1:
            print("1. Stand, make ace 11")
            print("2. Stand, make ace 1")
        print("3. Hit")
        print("4. Surrender")
    else:
        print("1. Stand")
        print("2. Hit")
        print("3. Surrender")

    choice = int(input("Your hand : "))
    if ace_count.size == 2 and choice == 1: choice = HAND_CHOICES[0]
    elif ace_count.size == 2 and choice == 2: choice = HAND_CHOICES[1]
    elif ace_count.size == 1 and choice == 1: choice = HAND_CHOICES[2]
    elif ace_count.size == 1 and choice == 2: choice = HAND_CHOICES[3]
    elif (is_have_ace and choice == 3) or (is_have_ace == False and choice == 2): choice = HAND_CHOICES[5]
    elif (is_have_ace and choice == 4) or (is_have_ace == False and choice == 3): choice = HAND_CHOICES[6]
    elif is_have_ace == False and choice == 1: choice = HAND_CHOICES[4]

def hit() -> np.ndarray:
    global SESSION_SHUFFLED, CARDS_OUT
    result = np.array([])
    result = np.append(result, SESSION_SHUFFLED[-1])
    CARDS_OUT = np.append(CARDS_OUT, SESSION_SHUFFLED[-1])
    SESSION_SHUFFLED = np.delete(SESSION_SHUFFLED, [-1])
    return result

def evaluate_hand(player_cards_val: int, dealer_cards_val: int):
    won = np.array([True, 'won'])
    lose = np.array([False, 'lose'])
    if 21 >= player_cards_val > dealer_cards_val: return won
    else: return lose


def play():
    global SESSION_SHUFFLED
    SESSION_SHUFFLED = _shuffle(np.array([]))
    
def reset():
    global SESSION_SHUFFLED, CARDS_OUT
    SESSION_SHUFFLED = np.array([])
    CARDS_OUT = np.array([])

play()