from deck import Deck

deck = Deck(Deck.PRESET_TRUCO)

hand = deck.draw(3)
for card in range(len(hand)):
    print(hand[card].to_string(True))

