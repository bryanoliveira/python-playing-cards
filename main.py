from truco import Truco

truco = Truco(2)

while not truco.is_done:
    print("Player " + str(truco.turn) + "'s turn.")
    obs = truco.observe(truco.turn)
    act = int(input(truco.available_actions_string(truco.turn) + ": "))
    reward = truco.act(truco.turn, act)
    print("Reward: " + str(reward))
    print()
