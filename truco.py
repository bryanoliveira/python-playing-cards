from deck import Deck


class Player:
    def __init__(self, index, team, name="Player"):
        self.index = index
        self.team = team
        self.name = name


class Truco:
    ACT_TRUCO = 3
    ACT_DECLINE = 4
    ACT_ACCEPT = 5

    def __init__(self, num_players, players=None, debug=True):
        self.actions_labels = ["Play card 0", "Play card 1", "Play card 2", "Raise", "Run away", "Accept raise"]
        self.deck = Deck(Deck.PRESET_TRUCO)
        self.num_players = num_players
        self.debug = debug
        self.players = [Player(i, int(i % 2)) for i in range(num_players)] if players is None else players

        self.is_done = False
        self.score = [0, 0]
        self.hands = [[] for i in range(self.num_players)]
        self.current_wins = []
        self.current_table = []
        self.bet = 1
        self.betting = False
        self.betting_bet = 0
        self.last_team_to_bet = -1
        self.betting_player = -1
        self.foot = 0
        self.turn = 0

        self.init_round()

    def reset(self):
        self.is_done = False
        self.score = [0, 0]
        self.hands = [[] for i in range(self.num_players)]
        self.current_wins = []
        self.current_table = []
        self.bet = 1
        self.betting = False
        self.betting_bet = 0
        self.last_team_to_bet = -1
        self.betting_player = -1
        self.foot = 0
        self.turn = 0

    def act(self, player, action):
        reward = 0

        if action == Truco.ACT_TRUCO:
            if self.last_team_to_bet == self.players[player].team:
                if self.debug:
                    print("Can't bet twice!")

            else:
                self.betting = True
                self.last_team_to_bet = self.players[player].team

                if self.betting_bet == 0:
                    self.betting_bet = 3 if self.bet == 1 else self.bet + 3
                    self.betting_player = player

                    if self.debug:
                        print("Player " + str(player) + " raised it to " + str(self.betting_bet))

                    self.next_turn()

                else:
                    self.bet = self.betting_bet

                    if self.betting_bet < 12:
                        self.betting_bet += 3

                        if self.debug:
                            print("Player " + str(player) + " raised it to " + str(self.betting_bet))

                        self.prev_turn()

                    else:
                        if self.debug:
                            print("Can't bet more!")

        elif action == Truco.ACT_DECLINE:
            reward, _ = self.win_round((self.players[player].team + 1) % 2)

            if self.debug:
                print("Player " + str(player) + " ran away.")

        elif action == Truco.ACT_ACCEPT:
            self.betting = False
            self.bet = self.betting_bet
            self.betting_bet = 0
            self.turn = self.betting_player
            self.betting_player = -1

            if self.debug:
                print("Player " + str(player) + " accepted " + str(self.bet))

        elif action >= len(self.hands[player]):
            if self.debug:
                print("Card already played, try another one!")

        else:
            card = self.hands[player][action]
            self.current_table.append(card)
            self.hands[player].remove(card)

            reward, next_player = self.check_hand()
            self.turn = next_player

        return reward * (-1 if self.players[player].team == 0 else 1)

    def observe(self, player):
        if self.debug:
            print("Your Score: " + str(self.score[self.players[player].team]))
            print("Their Score: " + str(self.score[(self.players[player].team + 1) % 2]))
            print("This round's wins: ", str(self.current_wins))

            print("Cards on the table: ")
            for card in range(len(self.current_table)):
                print("\t" + self.current_table[card].to_string())

            print("Cards on your hand: ")
            for card in range(len(self.hands[player])):
                print("\t(" + str(card) + ") " + self.hands[player][card].to_string())

        return [
            self.score[self.players[player].team],  # pontuação sua
            self.score[(self.players[player].team + 1) % 2],  # pontuação do adversário
            self.current_wins,  # pontuação das mãos
            self.current_table,  # cartas dessa mão
            self.hands[player]  # suas cartas
        ]

    def init_round(self):
        self.turn = self.foot
        self.current_wins = []
        self.current_table = []
        self.bet = 1
        self.betting = False
        self.betting_bet = 0
        self.last_team_to_bet = -1
        self.deck.reset()

        # distribui as mãos
        for hand in range(len(self.hands)):
            self.hands[hand] = self.deck.draw(3)

    def check_hand(self):
        # acabou a mão, vê quem ganhou
        if len(self.current_table) == self.num_players:
            winner = 0
            best = -1
            for play in range(len(self.current_table)):
                if self.current_table[play].value > best:
                    winner = play
                    best = self.current_table[play].value

            winner_player = (self.foot + winner) % self.num_players
            winner_team = self.players[winner_player].team

            self.current_table = []

            if len(self.current_wins) == 3 or winner_team in self.current_wins:
                return self.win_round(winner_team)
            else:
                self.current_wins.append(winner_team)

        return 0, (self.turn + 1) % self.num_players

    def win_round(self, team):
        reward = self.bet

        self.score[team] += self.bet
        self.foot = (self.foot + 1) % self.num_players

        if self.score[team] > 12:
            self.is_done = True

            if self.debug:
                print("Team " + str(team) + " won the game!")

        else:
            self.init_round()

            if self.debug:
                print("Team " + str(team) + " won the round!")

        return reward, self.foot

    def available_actions(self, player):
        if self.betting:
            if self.betting_bet < 12:
                return [Truco.ACT_TRUCO, Truco.ACT_DECLINE, Truco.ACT_ACCEPT]
            else:
                return [Truco.ACT_DECLINE, Truco.ACT_ACCEPT]
        else:
            actions = [i for i in range(len(self.hands[player]))]
            actions.append(Truco.ACT_TRUCO)
            actions.append(Truco.ACT_DECLINE)
            return actions

    def available_actions_string(self, player):
        str_actions = ""
        actions = self.available_actions(player)

        for action in range(len(actions)):
            str_actions += "(" + str(actions[action]) + ") " + self.actions_labels[actions[action]]
            if action < len(actions) - 1:
                str_actions += ", "

        return str_actions

    def next_turn(self):
        self.turn = (self.turn + 1) % self.num_players

    def prev_turn(self):
        self.turn = self.turn - 1 if self.turn > 0 else self.num_players - 1
