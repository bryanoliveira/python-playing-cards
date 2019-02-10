from deck import Deck


class Truco:
    ACT_TRUCO = 3
    ACT_ACCEPT = 0
    ACT_DECLINE = 1

    def __init__(self, num_players):
        self.deck = Deck(Deck.PRESET_TRUCO)
        self.num_players = num_players

        self.score = [0 for i in range(num_players)]

        self.hands = [[] for i in range(num_players)]
        self.current_wins = [-1 for i in range(num_players)]
        self.current_round = 0
        self.table = []
        self.bet = 1
        self.foot = 0

    def reset(self):
        self.deck.reset()
        self.score = [0 for i in range(self.num_players)]
        self.hands = [[] for i in range(self.num_players)]
        self.current_wins = [-1 for i in range(self.num_players)]
        self.current_round = 0
        self.table = []
        self.bet = 1

    def init_round(self):
        # distribui as mãos
        for hand in range(len(self.hands)):
            self.hands[hand] = self.deck.draw(3)

    def act(self, player, action):
        if action == Truco.ACT_TRUCO:
            if self.bet == 1:
                self.bet = 3
            elif self.bet < 12:
                self.bet += 3
            else:
                return False

        self.table.append(self.hands[player][action])

        # acabou a rodada, vê quem ganhou
        if len(self.table) == self.num_players:
            winner = 0
            best = -1
            for play in range(len(self.table)):
                if self.table[play].value > best:
                    winner = play
                    best = self.table[play].value

            self.score[(self.foot + winner) % self.num_players] += self.bet
            self.bet = 1

    def observe(self, player):
        return self.hands[player]
