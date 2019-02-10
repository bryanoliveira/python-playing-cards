from card import Card
import random


class Deck:
    PRESET_TRUCO = 0

    def __init__(self, preset=None):
        self.cards = []

        if preset is not None and preset == Deck.PRESET_TRUCO:
                force = 0
                # K, Q, J
                for number in range(11, 14):
                    for suit in range(4):
                        card = Card(number, suit, force)
                        self.cards.append(card)

                    force += 1

                # 1, 2, 3
                for number in range(1, 4):
                    for suit in range(4):
                        # Ace of spades
                        if number == 1 and suit == 1:
                            continue
                        else:
                            card = Card(number, suit, force)

                        self.cards.append(card)

                    force += 1

                self.cards.append(Card(7, Card.DIAMONDS, force))  # 7 of diamonds
                force += 1
                self.cards.append(Card(1, Card.SPADES, force))  # 7 of diamonds
                force += 1
                self.cards.append(Card(7, Card.HEARTS, force))  # 7 of diamonds
                force += 1
                self.cards.append(Card(4, Card.CLUBS, force))  # 7 of diamonds

        else:
            for number in range(1, 14):
                for suit in range(4):
                    card = Card(number, suit, number)
                    self.cards.append(card)

        self.deck = self.cards.copy()

    def draw(self, qtd=1):
        cards = []

        for i in range(qtd):
            card = self.deck[random.randint(0, len(self.deck) - 1)]
            self.deck.remove(card)
            cards.append(card)

        return cards

    def reset(self):
        self.deck = self.cards.copy()

    def show(self):
        for card in range(len(self.cards)):
            print(self.cards[card].to_string(True))
