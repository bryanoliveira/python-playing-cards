class Card:
    DIAMONDS = 0
    SPADES = 1
    HEARTS = 2
    CLUBS = 3

    def __init__(self, number, suit, value=None):
        self.suits = ["Diamonds", "Spades", "Hearts", "Clubs"]
        self.number = number
        self.suit = suit
        self.value = value if value is not None else number

    def to_string(self, show_value=False):
        if self.number == 1:
            card = "Ace of "
        elif self.number == 11:
            card = "J of "
        elif self.number == 12:
            card = "Q of "
        elif self.number == 13:
            card = "K of "
        else:
            card = str(self.number) + " of "

        card += self.suits[self.suit] + (" (" + str(self.value) + ")" if show_value else "")

        return card
