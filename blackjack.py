import random
import threading
import time
from datetime import datetime

# Card values
CARD_VALUES = {
    '2': 2, '3': 3, '4': 4, '5': 5, '6': 6,
    '7': 7, '8': 8, '9': 9, '10': 10,
    'J': 10, 'Q': 10, 'K': 10, 'A': 11
}

# Global flag to control clock thread
running = True


def create_deck():
    deck = list(CARD_VALUES.keys()) * 4
    random.shuffle(deck)
    return deck


def calculate_hand(hand):
    value = sum(CARD_VALUES[card] for card in hand)
    aces = hand.count('A')

    while value > 21 and aces:
        value -= 10
        aces -= 1

    return value


def deal_card(deck):
    return deck.pop()


def show_hand(player_hand, dealer_hand, reveal_dealer=False):
    print("\nYour hand:", player_hand, "Value:", calculate_hand(player_hand))
    if reveal_dealer:
        print("Dealer's hand:", dealer_hand, "Value:", calculate_hand(dealer_hand))
    else:
        print("Dealer's hand:", [dealer_hand[0], '?'])


# Blinking clock function
def clock(city):
    blink = True
    while running:
        now = datetime.now()
        colon = ":" if blink else " "
        time_str = now.strftime(f"%H{colon}%M{colon}%S")

        print(f"\r[{city}] Local Time: {time_str}", end="")
        blink = not blink
        time.sleep(1)


def blackjack():
    deck = create_deck()

    player_hand = [deal_card(deck), deal_card(deck)]
    dealer_hand = [deal_card(deck), deal_card(deck)]

    # Player turn
    while True:
        print("\n")
        show_hand(player_hand, dealer_hand)

        if calculate_hand(player_hand) > 21:
            print("You bust! Dealer wins.")
            return

        move = input("Hit or stand? (h/s): ").lower()
        if move == 'h':
            player_hand.append(deal_card(deck))
        elif move == 's':
            break
        else:
            print("Invalid input.")

    # Dealer turn
    while calculate_hand(dealer_hand) < 17:
        dealer_hand.append(deal_card(deck))

    # Final result
    show_hand(player_hand, dealer_hand, True)

    player_score = calculate_hand(player_hand)
    dealer_score = calculate_hand(dealer_hand)

    if dealer_score > 21:
        print("Dealer busts! You win!")
    elif player_score > dealer_score:
        print("You win!")
    elif player_score < dealer_score:
        print("Dealer wins!")
    else:
        print("It's a tie!")


if __name__ == "__main__":
    city = input("Where are you playing from? (Enter your city): ")

    print("\n=== Welcome to Blackjack ===")

    # Start clock thread
    clock_thread = threading.Thread(target=clock, args=(city,), daemon=True)
    clock_thread.start()

    try:
        while True:
            blackjack()
            again = input("\nPlay again? (y/n): ").lower()
            if again != 'y':
                break
    finally:
        running = False
        print("\nThanks for playing!")
