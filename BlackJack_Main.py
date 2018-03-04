'''
This is going to be a script for BlackJack
'''

# import required modules
from random import randint
from IPython.display import clear_output
import numpy as np
import os


# Define the classes I'll need for BlackJack. First, a deck of cards
class Deck():

	def __init__(self):
		self.cards=[['A',4],['K',4],['Q',4],['J',4],
			  [10,4],
			  [9,4],
			  [8,4],
			  [7,4],
			  [6,4],
			  [5,4],
			  [4,4],
			  [3,4],
			  [2,4]]
	
	def count(self):
		return sum([i[1] for i in self.cards])
	
	def draw(self):
		x=randint(1,self.count())
		counter=[i[1] for i in self.cards]
		counter=np.cumsum(counter)
		for index,value in enumerate(counter):
			if value < x:
				pass
			elif value >= x:
				self.cards[index][1]=self.cards[index][1]-1
				return self.cards[index][0]

class Player():

	def __init__(self,name,balance=50):
		self.name=name
		self.balance=balance

	def __str__(self):
		return('Account Owner: {0:6}\nAccount Balance: {1}'.format(self.name,self.balance))

	def deposit(self,amount):
		self.balance=self.balance+amount

	def withdraw(self,amount):
		if amount <= self.balance:
			return 'Insufficient Funds'
		else:
			self.balance=self.balance-amount

	def cards(self):
		print(self.cards)
	
	def set_cards(self,cards):
		self.cards=cards 

	def hit(self,deck):
		self.cards+=(deck.draw(),)
		
class Pot():
	
	def __init__(self):
		self.amount=0
		
	def ask_bet(self,*args):
		for i in args:
			bet=int(input('How much do you wish to bet? '))
			self.amount=self.amount+bet
		return bet
			
	def pay(self,payee,winner='player',typ='regular'):
		if winner=='player' and typ=='regular':
			payee.deposit(2*self.amount)
		elif winner=='player' and typ=='blackjack':
			payee.deposit(2.5*self.amount)
		else:
			payee.deposit(self.amount)
		self.amount=0

def convert_cards(cards):
	num_cards=list(cards)
	for index,value in enumerate(cards):
		if value=='K' or value=='Q' or value=='J':
			num_cards[index]=10
		elif value=='A':
			num_cards[index]=11
	return num_cards

def check_bust(cards):

	'''
	Check whether a set of cards (list) is bust.

	Input: list of cards in hand.

	Output: True if bust, False if not.
	'''

	cards=convert_cards(cards)
	if 11 in cards and sum(cards)>21:
		cards[cards.index(11)]=1
	if sum(cards)>21:
		return True
	return False

def give_sum(cards):

	cards=convert_cards(cards)
	if 11 in cards and sum(cards)>21:
		cards[cards.index(11)]=1
	return sum(cards)
	
def comp_play(cards):
	
	'''
	Check whether the computer should play. If its cards sum to 16 or below,
	then hit. Otherwise, stay.

	Input: the list that are the computer's cards

	Output: True or False - whether the computer should continue playing.
	'''
	cards=convert_cards(cards)
	if sum(cards)<=16:
		return True
	return False

def check_blackjack(cards):

	'''
	Function to check whether a set of cards is blackjack. This is important for payouts.
	'''

	if len(cards)==2 and 'A' in cards:
		if 'K' in cards or 'Q' in cards or 'J' in cards or 10 in cards:
			return True
	return False

def disp_game_state(pot,comp,*args,comp_disp=0):

	'''
	Function to display the current game state.
	
	Inputs:
		global pot
		comp
		*args - all players
		comp_disp - whether to show the computers face down card or not
	'''
	
	# determine whether to show computer's face down card or not
	if comp_disp==0:
		print("Dealer's Cards:\n[face down] , " + str(comp.cards[1:])[1:-1])
	elif comp_disp==1:
		print("Dealer's Cards:\n" + str(comp.cards)[1:-1])

	# print the amount in the pot
	print('\nAmount in pot: ' + str(pot.amount))
	
	# print what each player owns and the cards they have
	for i in args:
		print('\nCards: ' + str(i.cards)[1:-1])
		print(i)
		
def play_round(comp,*args):
	
	global pot
	global deck
	
	# give players and computer two cards each
	comp_init=(deck.draw(),deck.draw())
	comp.set_cards(comp_init)
	
	for player in args:
		player_init=(deck.draw(),deck.draw())
		player.set_cards(player_init)
	
	for player in args:
		disp_game_state(pot,comp,player)


	# now ask for bets
	for player in args:
		bet=pot.ask_bet(player)
		player.withdraw(bet)
	
	# players play
	for player in args:
		while not(check_bust(player.cards)):
			os.system('clear')
			clear_output()
			disp_game_state(pot,comp,player)
			temp=input('Hit? [y/n]').lower()
			if temp=='y':
				player.hit(deck)
				continue
			elif temp=='n':
				break
		else:
			pot.pay(comp, winner='computer')
			print(player.name + ' is bust')
			return True


	# computer plays, but only if the player is not bust
	if not(check_bust(args[0].cards)):

		# keep going whilst the computer should play
		while comp_play(comp.cards):
			input('Press Enter to Continue...')
			os.system('clear')
			clear_output()
			comp.hit(deck)
			disp_game_state(pot,comp,args[0],comp_disp=1)


		# Check for dealer bust
		if check_bust(comp.cards):
			pot.pay(args[0],winner='player')
			print(player.name + ' wins. Dealer is bust')
			return True

		# now check who won, and pay out

		# calculate sum of cards
		pcards=give_sum(args[0].cards)
		print('pcards: ' + str(pcards))
		ccards=give_sum(comp.cards)
		print('ccards: ' + str(ccards))

		# if player's sum is greater than dealer's it could blackjack or regular win
		if  pcards > ccards:
			if check_blackjack(args[0].cards):
				pot.pay(args[0],winner='player',typ='blackjack')
				print('Player wins. Blackjack!')
			else:
				pot.pay(args[0],winner='player',typ='regular')
				print('Player wins.')
			return True

		# if player's sum is equal, then return bet
		elif pcards == ccards:
			pot.pay(args[0],winner='tie')
			print('Tie. Bet returned.')
			return True

		# otherwise, computer wins. pay computer
		else:
			pot.pay(comp,winner='dealer')
			print('Dealer wins. Bet lost.')
			return True

# initialise required objects
deck=Deck()
pot=Pot()

# ask for the player's name!
name=input('Please Enter Your Name: ')

# initialise player and dealers
comp=Player('Computer',100)
p1=Player(name,100)

# play the game!
# while True:
# 	if play_round(comp,p1):
# 		x=input('Another round? [y/n]').lower()
# 		if x=='n':
# 			break

# print(p1)
