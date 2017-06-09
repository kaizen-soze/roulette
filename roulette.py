import math
import random
from colorama import init, reinit, deinit
from colorama import Fore, Back, Style

class Pocket:
	''' Class that imitates the spots in a roulette wheel'''

	def __init__(self, number, number_type, color):
		self.number = number
		self.number_type = number_type
		self.color = color

	def __iter__(self):
		return self

	def __repr__(self):
		return str('{0} | {1} | {2}'.format(self.number, self.number_type, self.color))

	def __next__(self):
		if self.number == 36:
			raise StopIteration
		else:
			self.number += 1
			return self

class Logic:
	''' Class that contains game logic '''

	def __init__(self, bankroll=100):
		self.bankroll = bankroll
		self.previous_numbers = []
		self.bet_type = 0
		self.bet_value = -1
		self.bet_selection = -1
		self.multiplier = 2
		self.game_mode = 0
		self.probability_threshold = -1
		self.loops = -1
		self.strategy = 0
		self.won_last_bet = None
		self.won = 0
		self.lost = 0
		self.most_money = 0
		self.spins = 0
		self.watched = 0
		self.base_level_bet = 10

	def automaticSpin(self):
		winner = False
		zero = False
		bet_on_this_spin = False

		wheel = Logic.chooseWheel(self)
		chosen_color = None

		# Exact number
		
		# Color
		# Bet based on probability of next color being of a certain type
		if(self.bet_type == 2 and self.strategy == 1):
			self.multiplier = 2
			chosen_color = Logic.findColor(self)

			# if this is either of the first two spins, skip betting this spin
			if(len(self.previous_numbers) == 0):
				bet_on_this_spin = False
			elif(chosen_color == None):
				bet_on_this_spin = False
			
			# if the percentage of a color change is greater than the threshold, bet the minimum amount on the opposite color
			chance_of_preferred_color = .48648
			streak = Logic.findColorSequence(self)
			color_to_bet_on = None
			
			calculated_probability = math.pow(chance_of_preferred_color, streak)
			
			if(calculated_probability <= self.probability_threshold and chosen_color is not None):
				bet_on_this_spin = True
				color_to_bet_on = "red" if(chosen_color == "black") else "black"
			
			# calculate the chance of the next spin changing color
			if(bet_on_this_spin == True):
				if(self.bet_value == -1):
					self.bet_value = self.base_level_bet

				# if you lost your last bet, double down
				if(self.won_last_bet == False):
					self.bet_value = self.bet_value * 2

			if(bet_on_this_spin == False):
				self.watched += 1

			# Evaluate spin
			if(bet_on_this_spin == True):	
				print("Betting ${0} on {1}".format(self.bet_value, color_to_bet_on))
				self.bankroll = self.bankroll - self.bet_value

			# Spin the wheel!
			ball = Logic.simpleSpin(self)
			print("Spun the wheel and rolled a {0} {1}".format(wheel[ball].color, wheel[ball].number))

			if(bet_on_this_spin == True):
				if(wheel[ball].color == color_to_bet_on):
					winner = True
					self.won_last_bet = True
				elif(wheel[ball].number == 0):
					zero = True
				else:
					winner = False
					self.won_last_bet = False

		# Random color
		if(self.bet_type == 2 and self.strategy == 2):
			to_bet = random.randint(0,1)
			bet_on_this_spin = True

			if(to_bet == 0):
				bet_on_this_spin = False
			else:
				bet_on_this_spin = True
			
			if(bet_on_this_spin == True):
				self.bet_value = 10
				temp_multiplier = random.randint(1,5)

				proposed_bet = self.bet_value * temp_multiplier
				proposed_bankroll = self.bankroll - proposed_bet

				if(proposed_bankroll > 0):
					self.bet_value = proposed_bet
				else:
					self.bet_value = 10
				
				#print("Proposed bet is ${0} and proposed bankroll is ${1}".format(proposed_bet, proposed_bankroll))

			color_to_bet_on = None

			random_color = random.randint(0,49)

			if(random_color == 0):
				color_to_bet_on = "green"
			elif(random_color % 1 == 0):
				color_to_bet_on = "black"
			elif(random_color % 2 == 0):
				color_to_bet_on = "red"
			
			if(bet_on_this_spin == False):
				self.watched += 1

			# Evaluate spin
			if(bet_on_this_spin == True):	
				print("Betting ${0} on {1}".format(self.bet_value, color_to_bet_on))
				self.bankroll = self.bankroll - self.bet_value

			# Spin the wheel!
			ball = Logic.simpleSpin(self)
			print("Spun the wheel and rolled a {0} {1}".format(wheel[ball].color, wheel[ball].number))

			if(bet_on_this_spin == True):
				if(wheel[ball].color == color_to_bet_on):
					winner = True
					self.won_last_bet = True
				elif(wheel[ball].number == 0):
					zero = True
				else:
					winner = False

		# High/Low
		
		if(self.bankroll > self.most_money):
			self.most_money = self.bankroll

		if(bet_on_this_spin == True):
			if winner:
				amount_won = (self.bet_value * self.multiplier)
				self.bankroll += amount_won
				self.won += 1
				self.bet_value = self.base_level_bet
				print("Winner! Won ${0}. New bankroll is ${1}".format(amount_won, self.bankroll))
			elif zero:
				returned_bet = int(self.bet_value / 2)
				print("0! Half your bet, ${0},returned.".format(returned_bet))
				self.bankroll += returned_bet
				self.lost += 1
				self.bet_value = self.base_level_bet
			else:
				print("Loser! You bet on {0}".format(color_to_bet_on))
				self.lost += 1

		#nada = input("Press [Enter] to continue")

		# if you're out of money, tell how far you got before going bust
		if(self.bankroll <= 0):
			print("You're out of money after {0} spins! You won {1} rounds, lost {2} rounds, and watched {3} rounds. At one point you had had ${4}.".format(self.spins, self.won, self.lost, self.watched, self.most_money))
			exit()

		return

	def chooseWheel(choice='euro_wheel'):
		# Eventually there should be various types of wheels, and these should be objects in the roulette class
		euro_wheel = [
			Pocket(0, "zero", "green"),
			Pocket(26, "even", "black"),
			Pocket(3, "odd", "red"),
			Pocket(35, "odd", "black"),
			Pocket(12, "even", "red"),
			Pocket(28, "even", "black"),
			Pocket(7, "odd", "red"),
			Pocket(29, "odd", "black"),
			Pocket(18, "even", "red"),
			Pocket(22, "even", "black"),
			Pocket(9, "odd", "red"),
			Pocket(31, "odd", "black"),
			Pocket(14, "even", "red"),
			Pocket(20, "even", "black"),
			Pocket(1, "odd", "red"),
			Pocket(33, "odd", "black"),
			Pocket(16, "even", "red"),
			Pocket(24, "even", "black"),
			Pocket(5, "odd", "red"),
			Pocket(10, "even", "black"),
			Pocket(23, "odd", "red"),
			Pocket(8, "even", "black"),
			Pocket(30, "even", "red"),
			Pocket(11, "odd", "black"),
			Pocket(36, "even", "red"),
			Pocket(13, "odd", "black"),
			Pocket(27, "odd", "red"),
			Pocket(6, "even", "black"),
			Pocket(34, "even", "red"),
			Pocket(17, "odd", "black"),
			Pocket(25, "odd", "red"),
			Pocket(2, "even", "black"),
			Pocket(21, "odd", "red"),
			Pocket(4, "even", "black"),
			Pocket(19, "odd", "red"),
			Pocket(15, "odd", "black"),
			Pocket(32, "even", "red")	
		]

		#for space in euro_wheel:
		#	print("{0}, {1}".format(space.number, space.color))

		return euro_wheel

	def findColor(self):
		color_to_seek = None

		if(len(self.previous_numbers) > 0):
			last_pocket = self.previous_numbers[-1]
			color_to_seek = last_pocket.color

		if(color_to_seek == 'green'):
			return None
		else:
			return color_to_seek

	def findColorSequence(self):
		streak = 0
		euro_wheel = Logic.chooseWheel()
		color_to_seek = None

		if(len(self.previous_numbers) > 0):
			last_pocket = self.previous_numbers[-1]
			color_to_seek = last_pocket.color

		if(color_to_seek == 'green'):
			return 0

		for x in reversed(self.previous_numbers):
			if(color_to_seek == 'red' and x.color == 'red'):
				streak += 1
			elif(color_to_seek == 'red' and (x.color == 'black' or x.color == 'green')):
				return streak
			elif(color_to_seek == 'black' and x.color == 'black'):
				streak += 1
			elif(color_to_seek == 'black' and (x.color == 'red' or x.color == 'green')):
				return streak
	
		return streak

	def printStats(self):
		
		# initialize colorama
		reinit()

		width = 10

		print("Previous Numbers: ")
		# break what you're fetching into fifteen numbers per row at the most
		# algorithmically determine the number of items to print, and create formatting instructions
		# if you reach the maximum number of items, create a new row

		# maximum height is 16
		
		if(len(self.previous_numbers) > 0):
				for x in reversed(self.previous_numbers):
					if(x.color == 'red'):
						print(Back.RED + "{0: <3}".format(x.number))
					elif(x.color == 'black'):
						print(Back.BLACK + "     {0: <3}".format(x.number))
					else:
						print(Back.GREEN + "  {0: <3}".format(x.number))
		print(Style.RESET_ALL)

		deinit()

	def simpleSpin(self):
		# Pick a winning value
		ball = random.randint(0,36)
		wheel = Logic.chooseWheel()
		self.spins += 1

		# Add it to the list of previous numbers
		self.previous_numbers.append(wheel[ball])

		return ball

	def bet(self):
		# initialize colorama
		color = init()

		# clear the screen
		Screens.clear()

		# Select game mode
		Screens.selectMode(self)

		Screens.clear()		
		# Main Game Loop
		while(self.bet_type != 99):
			# Choose the game type
			Screens.chooseGameType(self)

			Screens.clear()

			# Find out how much they bet and what they're betting on
			Screens.placeBet(self)
			Screens.selectBet(self)
			Logic.resetValues(self)

		Screens.exitGame(self)
			

	def resetValues(self):
		self.bet_type = 0
		self.bet_value = -1
		self.bet_selection = -1
		self.multiplier = 2
		self.game_mode = 0
	
	def probabilityStrategy(self):
		if(self.strategy == 1):
			Screens.setProbability(self)

			print("\nThe computer will now simulate {0} rounds of roulette. \nA bet will be placed when there is a >= {1}% probability that the next number will break the combo\n".format(self.loops, self.probability_threshold))
			
			nada = input("Press [Enter] to continue")

		while(self.spins <= self.loops):
			Logic.automaticSpin(self)

		print("{0} loops completed.\n".format(self.loops))
		Screens.displayBankroll(self)

		print("After {0} spins, you won {1} rounds, lost {2} rounds, and watched {3} rounds. At one point you had had ${4}.".format(self.spins, self.won, self.lost, self.watched, self.most_money))
		exit()

	def spin(self, bet_type, bet_value, bet_selection, multiplier, wheel):

		# Pick a winning value
		ball = random.randint(0,36)

		# Add it to the list of previous numbers
		self.previous_numbers.append(wheel[ball])

		Screens.clear()
		print("The ball whirls around the roulette table, eventually settling on...")

		if(wheel[ball].color == "red"):
			print(Back.RED + '{0} | {1} | {2}'.format(wheel[ball].number, wheel[ball].number_type, wheel[ball].color))
		elif(wheel[ball].color == "green"):
			print(Back.GREEN + '{0} | {1} | {2}'.format(wheel[ball].number, wheel[ball].number_type, wheel[ball].color))
		else:
			print('{0} | {1} | {2}'.format(wheel[ball].number, wheel[ball].number_type, wheel[ball].color))

		print(Back.RESET)
		winner = False
		zero = False

		if(self.bet_selection > -2):
			# Exact number
			if(self.bet_type == 1):
				if(wheel[ball].number == self.bet_selection):
					winner = True
				elif(wheel[ball].number == 0):
					zero = True

			# Color
			if(self.bet_type == 2):
				chosen_color = "red" if(self.bet_selection == 1) else "black"
				
				if(wheel[ball].color == chosen_color):
					winner = True
				elif(wheel[ball].number == 0):
					zero = True

			# High/Low
			if(self.bet_type == 3):
				number_maximum = 36 if(self.bet_selection == 1) else 18
				number_minimum = 19 if(self.bet_selection == 1) else 1
				
				if(wheel[ball].number >= number_minimum and wheel[ball].number <= number_maximum):
					winner = True
				elif(wheel[ball].number == 0):
					zero = True

			# Even/Odd
			if(self.bet_type == 4):
				selection_value = "even" if(self.bet_selection == 1) else "odd"
				if(wheel[ball].number_type == selection_value):
					winner = True
				elif(wheel[ball].number_type == "zero"):
					zero = True

			if winner:
				self.bankroll += (self.bet_value * self.multiplier)
				print("Congratulations! You win! Bankroll: ${0}".format(self.bankroll))
			elif zero:
				print("\n\nBankroll: ${0}\n".format(self.bankroll))
				print("Zoinks! You hit a zero! What rotten luck! Here, have half your bet back.\n\n")
				print("Adding ${0} to your bankroll.".format(int((self.bet_value / 2))))
				self.bankroll += int((self.bet_value / 2))
				print("Bankroll: ${0}\n".format(self.bankroll))
				print("We're pretty confident we'll get it back in the long run anyway...")
				
			else:
				print("Better luck next time. You lost! Bankroll: ${0}".format(self.bankroll))

			if(self.bankroll == 0):
				Screens.clear()
				print("Ooh, you're out of money! Looks like the house won again. Sucker.")
				exit()

		nada = input("Press [Enter] to continue")
		Screens.clear()

		return

class Screens:
	''' Class that contains screens for the game '''

	def __init__(self):
		pass

	def clear():
		print(chr(27) + "[2J")

	def chooseGameType(self):

		while(self.bet_type == 0):
			print("Bankroll: ${0}\n\n".format(self.bankroll))
			Logic.printStats(self)
			print("What type of bet would you like to place?")
			print("1. Exact Number (Pays out 35x your bet)")
			print("2. Color (Pays out 2x your bet)")
			print("3. High/Low (Pays out 2x your bet)")
			print("4. Even/Odd (Pays out 2x your bet)")
			print("5. Skip this round")
			print("\n99. Quit")

			try:
				self.bet_type = int(input("> "))
			except ValueError:
				self.bet_type = 0
				Screens.clear()
				print("Sorry, integers only\n")
				continue

			if(self.bet_type < 1 or self.bet_type > 99):
				self.bet_type = 0
				Screens.clear()
				print("Inappropriate selection\n")

			if(self.bet_type == 1):
				self.multiplier = 35
			else:
				self.multiplier = 2

			if(self.bet_type == 99):
				Screens.clear()
				print("We're sorry to see you go!")
				if(self.bankroll > 0):
					print("Mainly because you escaped with ${0}".format(self.bankroll))
				else:
					print("Come back when you manage to scrape some more money together")

				exit()

		return

	def displayBankroll(self):
		print("Your total bankroll is ${0}\n\n".format(self.bankroll))

	def exitGame(self):
		Screens.clear()
		print("We're sorry to see you go!")
		if(self.bankroll > 0):
			print("Mainly because you escaped with ${0}".format(self.bankroll))
		else:
			print("Come back when you manage to scrape some more money together")

		exit()

	def placeBet(self):
		Screens.displayBankroll(self)
		Logic.printStats(self)

		# If the user has chosen to skip this round, set the values needed for the other two loops and spin the ball
		if(self.bet_type == 5):
			self.bet_value = 0
			self.bet_selection = -2

		while(self.bet_value == -1):
			print("How much would you like to bet?")
			try:
				self.bet_value = int(input("> $"))
			except ValueError:
				self.bet_type = -1
				Screens.clear()
				print("Sorry, integers only\n")
				continue

			if(self.bet_value > self.bankroll):
				Screens.clear()
				print("You can't bet more money than you actually have. Obviously. \n")
				print("You entered ${0} but only have ${1}".format(self.bet_value, self.bankroll))
				self.bet_value = -1

		# update bankroll value
		self.bankroll -= self.bet_value

		return

	def selectBet(self):
		while(self.bet_selection == -1):
			if(self.bet_type == 1):
				Screens.clear()
				print("Bankroll: ${0}\n\n".format(self.bankroll))
				Logic.printStats(self)
				print("Bet: ${0}\n\n".format(self.bet_value))
				print("Betting Mode: Exact Number\n")
				print("To win, you must choose the exact number that the roulette ball lands on. Choose wisely.\n")

				try:
					self.bet_selection = int(input("> "))
				except ValueError:
					self.bet_selection = -1
					Screens.clear()
					print("Sorry, numbers only\n")
					continue

				if(self.bet_selection < 0 or self.bet_selection > 36):
					self.bet_selection = -1
					Screens.clear()
					print("You must select one number between 0 and 36\n")

			elif(self.bet_type == 2):
				Screens.clear()
				print("Bankroll: ${0}\n\n".format(self.bankroll))
				Logic.printStats(self)
				print("Bet: ${0}\n\n".format(self.bet_value))
				print("Betting Mode: Color\n")
				print("Place your bet.")
				print("1. Red")
				print("2. Black\n")

				try:
					self.bet_selection = int(input("> "))
				except ValueError:
					self.bet_selection = -1
					Screens.clear()
					print("Sorry, numbers only\n")
					continue

				if(self.bet_selection > 2):
					self.bet_selection = -1
					Screens.clear()
					print("Red or black. It's not a hard choice.\n")

			elif(self.bet_type == 3):
				Screens.clear()
				print("Bankroll: ${0}\n\n".format(self.bankroll))
				Logic.printStats(self)
				print("Bet: ${0}\n\n".format(self.bet_value))
				print("Betting Mode: High/Low\n")
				print("Place your bet.")
				print("1. High (19 - 36)")
				print("2. Low (1 - 18)\n")

				try:
					self.bet_selection = int(input("> "))
				except ValueError:
					self.bet_selection = -1
					Screens.clear()
					print("Sorry, numbers only\n")
					continue

				if(self.bet_selection > 2):
					self.bet_selection = -1
					Screens.clear()
					print("Pick high or pick low. It's not a hard choice.\n")

			elif(self.bet_type == 4):
				Screens.clear()
				print("Bankroll: ${0}\n\n".format(self.bankroll))
				Logic.printStats(self)
				print("Bet: ${0}\n\n".format(self.bet_value))
				print("Betting Mode: Even/Odd\n")
				print("Place your bet.")
				print("1. Even")
				print("2. Odd\n")

				try:
					self.bet_selection = int(input("> "))
				except ValueError:
					self.bet_selection = -1
					Screens.clear()
					print("Sorry, numbers only\n")
					continue

				if(self.bet_selection > 2):
					self.bet_selection = -1
					Screens.clear()
					print("Even or odd, chuckles. It's not a hard choice.\n")

		Logic.spin(self, self.bet_type, self.bet_value, self.bet_selection, self.multiplier, Logic.chooseWheel())

		return

	def selectMode(self):

		while(self.game_mode == 0):

			print("Select Game Mode")
			print("1. Manual")
			print("2. Automatic")
			
			print("\n99. Quit")

			try:
				self.game_mode = int(input("> "))
			except ValueError:
				self.game_mode = 0
				Screens.clear()
				print("Sorry, integers only\n")
				continue

			if(self.game_mode > 2 and self.game_mode != 99):
				self.game_mode = 0
				Screens.clear()
				print("Inappropriate selection\n")

			if(self.game_mode == 1):
				return
			else:
				Screens.clear()
				Screens.selectStrategy(self)

			if(self.game_mode == 99):
				Screens.clear()
				print("We're sorry to see you go!")
				if(self.bankroll > 0):
					print("Mainly because you escaped with ${0}".format(self.bankroll))
				else:
					print("Come back when you manage to scrape some more money together")

				exit()

		return

	def selectStrategy(self):

		while(self.strategy == 0):

			print("Select Strategy")
			print("1. Probabilities")
			print("2. Random")
			
			print("\n99. Quit")

			try:
				self.strategy = int(input("> "))
			except ValueError:
				self.strategy = 0
				Screens.clear()
				print("Sorry, integers only\n")
				continue

			if(self.strategy > 3 and self.strategy != 99):
				self.strategy = 0
				Screens.clear()
				print("Inappropriate selection\n")

			# Probability of color
			if(self.strategy == 1):
				self.bet_type = 2
				Screens.setLoop(self)
				Logic.probabilityStrategy(self)
			# Random color
			if(self.strategy == 2):
				self.bet_type = 2
				Screens.setLoop(self)
				Logic.probabilityStrategy(self)
			elif(self.strategy == 99):
				Screens.clear()
				print("We're sorry to see you go!")
				if(self.bankroll > 0):
					print("Mainly because you escaped with ${0}".format(self.bankroll))
				else:
					print("Come back when you manage to scrape some more money together")

				exit()

		return

	def setLoop(self):

		while(self.loops == -1):
			print("\nHow many times do you want this strategy to run?")
			try:
				self.loops = int(input("> "))
			except ValueError:
				self.loops = -1
				Screens.clear()
				print("Sorry, integers only\n")
				continue

		return

	def setProbability(self):

		while(self.probability_threshold == -1):
			print("\nAt what percentage do you want the computer to place a wager? For 23%, enter .23")
			print("Probabilities: \n")
			print("2 consecutive colors: 24%")
			print("3 consecutive colors: 12%")
			print("4 consecutive colors:  6%")
			print("5 consecutive colors:  3%")
			print("6 consecutive colors:  2%")
			print("7 consecutive colors:  1%")
			try:
				self.probability_threshold = float(input("> "))
			except ValueError:
				self.loops = -1
				Screens.clear()
				print("Sorry, integers only\n")
				continue

		return