from roulette import Logic

bankroll = 100

game = Logic(bankroll)

while(bankroll > 0):
	Logic.bet(game)
