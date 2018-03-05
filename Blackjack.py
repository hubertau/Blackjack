'''
This is going to be a simple script for BlackJack involving one player and one dealer.
'''

# import required modules
import os
from random import randint
from IPython.display import clear_output
import numpy as np


# Define the classes I'll need for BlackJack. First, a deck of cards
class Deck:

    '''
    This class will contain a deck of cards, for a specified number of decks.
    The default number of decks is 2.
    '''

    def __init__(self, n=2):

        # store number of decks
        self.num = n

        # initialise deck with n decks
        self.cards = [['A', 4*n], ['K', 4*n], ['Q', 4*n], ['J', 4*n],\
                    [10, 4*n],\
                    [9, 4*n],\
                    [8, 4*n],\
                    [7, 4*n],\
                    [6, 4*n],\
                    [5, 4*n],\
                    [4, 4*n],\
                    [3, 4*n],\
                    [2, 4*n]]

    # define the count method to allow quick check of how many cards are in
    # the deck
    def count(self):
        '''
        Returns count of number of cards in the deck.
        '''
        return sum([i[1] for i in self.cards])

    # procedure to draw a card from the deck.
    def draw(self):

        '''
        Returns a randomly selected card from the cards that are left.
        '''

        # first, generate a random number between 1 and the number of cards in the deck.
        card_num = randint(1, self.count())

        # the next part generates a cumulative sum list for the number cards of each type.
        # Since the random number generated suffices as a random choice of card, by matching
        # with the cumulative sum of cards a card value can be picked out.
        counter = [i[1] for i in self.cards]

        # np = numpy
        counter = np.cumsum(counter)

        # now for the first value in counter that is greater than or equal to the random
        # integer, the random integer must then indicate the card type of that index. So
        # return that card.
        for index, value in enumerate(counter):
            if value < card_num:
                pass
            elif value >= card_num:
                self.cards[index][1] = self.cards[index][1]-1
                return self.cards[index][0]

    def reset(self):

        '''
        Method to reset the cards to the original deck.
        '''

        for i in self.cards:
            i[1] = 4*self.num

class Player:

    '''
    This player class will be what the computer and the player will be assigned,
    allowing deposits, withdrawals, etc.
    '''

    def __init__(self, name, balance=100):

        '''
        Initialise name, balance, and leave cards empty.
        '''

        self.name = name
        self.balance = balance
        self.cards = None

    def __str__(self):

        '''
        Change print function to display owner and balance
        '''

        return 'Account Owner: {0:6}\nAccount Balance: {1}'.format(self.name, self.balance)

    def deposit(self, amount):

        '''
        Deposit amount into player's account.
        '''

        self.balance = self.balance+amount

    def withdraw(self, amount):

        '''
        Withdraw funds from account. Disallow if there are insufficient funds.
        '''

        if amount > self.balance:
            return 'Insufficient Funds'
        else:
            self.balance = self.balance-amount

    def show_cards(self):

        '''
        Print the cards that the player has.
        '''

        print(self.cards)

    def set_cards(self, cards):

        '''
        Set the cards of the player. This will be done at the beginning of each
        round.
        '''

        self.cards = cards

    def hit(self, deck):


        '''
        Hit function for a player. This draws a card fom the deck randomly,
        and shuffles the deck if the number of cards in the deck is less than
        half the original number.
        '''

        self.cards += (deck.draw(),)
        if deck.count() < (deck.num*52)/2:
            deck.reset()
            print('Deck Reshuffled')

class Pot:

    '''
    Pot class to contain the pot of money that is being bet, and
    subsequently to be distributed.
    '''

    def __init__(self):

        '''
        Initialise. Set pot to contain no money.
        '''

        self.amount = 0

    def ask_bet(self, *args):

        '''
        Ask for a bet from the player. Do not accept bet unless it is
        (a) an integer, and
        (b) less than the total available funds.

        Then add to to pot and return the bet asked for. This will be used
        in later script to withdraw from the player.
        '''

        for i in args:
            while True:
                bet = int(input('How much do you wish to bet? '))
                if bet > i.balance:
                    print('You have insufficient funds. Please try again.')
                    continue
                elif bet == 0:
                    print('Cannot enter 0 bet.')
                    continue
                self.amount = self.amount+bet
                break
        return bet

    def pay(self, payee, winner='player', typ='regular'):

        '''
        Pay a deisgnated payee. Depending on the winner and type of win, pay
        different amounts.

        If the winner is the player, then the payout is 1:1 or 3:2 depending
        on whether it is a regular win or a blackjack win.

        Otherwise, if it is the dealer, just dump amount into computer's bank.
        '''

        if winner == 'player' and typ == 'regular':
            payee.deposit(2*self.amount)
        elif winner == 'player' and typ == 'blackjack':
            payee.deposit(2.5*self.amount)
        else:
            payee.deposit(self.amount)
        self.amount = 0

def convert_cards(cards):

    '''
    Simple function to convert royal cards to numbers.
    '''

    num_cards = list(cards)
    for index, value in enumerate(cards):
        if value == 'K' or value == 'Q' or value == 'J':
            num_cards[index] = 10
        elif value == 'A':
            num_cards[index] = 11
    return num_cards

def check_bust(cards):

    '''
    Check whether a set of cards (list) is bust.

    Input: list of cards in hand.

    Output: True if bust, False if not.
    '''

    # convert cards from letters to numbers
    cards = convert_cards(cards)

    # There may be multiple Aces in a hand. So utilise while loop.
    # If hand is bust, decrease sum by 10 until it is not.
    while 11 in cards:

        # If sum is over 21, then replace 11 with lowest index by 1.
        # But break if sum is not over 21 and there is still an 11,
        # otherwise the while loop will run forever.
        if sum(cards) > 21:
            cards[cards.index(11)] = 1
        else:
            break

    if sum(cards) > 21:
        return True
    return False

def give_sum(cards):

    '''
    Returns the sum of the cards in a hand.
    '''

    # convert cards from letters to numbers
    cards = convert_cards(cards)

    # If sum is over 21, then replace 11 with lowest index by 1.
    # But break if sum is not over 21 and there is still an 11,
    # otherwise the while loop will run forever.
    while 11 in cards:
        if sum(cards) > 21:
            cards[cards.index(11)] = 1
        else:
            break

    return sum(cards)

def comp_play(cards):

    '''
    Check whether the computer should play. If its cards sum to 16 or below,
    then hit. Otherwise, stay.

    Input: the list that are the computer's cards

    Output: True or False - whether the computer should continue playing.
    '''

    cards = convert_cards(cards)
    if sum(cards) <= 16:
        return True
    return False

def check_blackjack(cards):

    '''
    Function to check whether a set of cards is blackjack. This is important for payouts.
    '''

    if len(cards) == 2 and 'A' in cards:
        if 'K' in cards or 'Q' in cards or 'J' in cards or 10 in cards:
            return True
    return False

def disp_game_state(pot, comp, *args, comp_disp=0):

    '''
    Function to display the current game state.

    Inputs:
        global pot
        comp
        *args - all players
        comp_disp - whether to show the computers face down card or not
    '''

    # determine whether to show computer's face down card or not
    if comp_disp == 0:
        print("Dealer's Cards:\n[face down] , " + str(comp.cards[1:])[1:-1])
    elif comp_disp == 1:
        print("Dealer's Cards:\n" + str(comp.cards)[1:-1])

    # print the amount in the pot
    print('\nAmount in pot: ' + str(pot.amount))

    # print what each player owns and the cards they have
    for i in args:
        print('\nCards: ' + str(i.cards)[1:-1])
        print(i)
        print('')

def play_round(comp, *args):

    '''
    Play one round.
    '''

    # call global for pot and deck. These will need to be
    # modified for any future rounds
    global pot
    global deck

    # give players and computer two cards each
    comp_init = (deck.draw(), deck.draw())
    comp.set_cards(comp_init)

    for player in args:
        player_init = (deck.draw(), deck.draw())
        player.set_cards(player_init)

    # now ask for bets
    for player in args:
        print(player)
        bet = pot.ask_bet(player)
        player.withdraw(bet)

    # Players play
    for player in args:

        # Keep playing whilst the player is not bust
        while not check_bust(player.cards):

            if len(player.cards) == 5:

                # Clear outputs
                os.system('clear')
                clear_output()

                # Display game state
                disp_game_state(pot, comp, player)

                pot.pay(player, winner='player')
                print(player.name + ' has 5 cards and so wins.\nNew Account Balance: {}'\
                    .format(args[0].balance))
                return True

            # Clear outputs
            os.system('clear')
            clear_output()

            # Display game state
            disp_game_state(pot, comp, player)

            # Ask whether to hit or not
            temp = input('Hit? [y/n]').lower()

            # If yes, then hit and return to top of while loop. If not,
            # then check if bust
            if temp == 'y':
                player.hit(deck)
                continue
            elif temp == 'n':
                break
        else:

            # Clear outputs
            os.system('clear')
            clear_output()

            # Display game state
            disp_game_state(pot, comp, player)

            pot.pay(comp, winner='computer')
            print(player.name + ' is bust\nNew Account Balance: {}'.format(args[0].balance))
            return True


    # Now computer plays

    if comp_play(comp.cards):

        # keep going whilst the computer should play
        input('Press Enter to Continue...')
        while comp_play(comp.cards):

            # Clear outputs
            os.system('clear')
            clear_output()

            comp.hit(deck)
            disp_game_state(pot, comp, args[0], comp_disp=1)
            input('Press Enter to Continue...')
    else:
        input('Press Enter to Continue...')
        os.system('clear')
        clear_output()
        disp_game_state(pot, comp, args[0], comp_disp=1)

    # Now that play is over, check for dealer bust
    if check_bust(comp.cards):
        pot.pay(args[0], winner='player')
        print(player.name + ' wins. Dealer is bust.\nNew Account Balance: {}'\
            .format(args[0].balance))
        return True

    # now check who won, and pay out

    # calculate sum of cards
    pcards = give_sum(args[0].cards)
    ccards = give_sum(comp.cards)

    # if player's sum is greater than dealer's it could blackjack or regular win
    if  pcards > ccards:
        if check_blackjack(args[0].cards):
            pot.pay(args[0], winner='player', typ='blackjack')
            print(args[0].name + ' wins. Blackjack!\nNew Account Balance: {}'\
                .format(args[0].balance))
        else:
            pot.pay(args[0], winner='player', typ='regular')
            print(args[0].name + ' wins.\nNew Account Balance: {}'.format(args[0].balance))
        return True

    # if player's sum is equal, then return bet
    elif pcards == ccards:
        if check_blackjack(args[0].cards) and check_blackjack(comp.cards):
            pot.pay(args[0], winner='tie')
            print('Tie. Bet returned.\nAccount Balance: {}'.format(args[0].balance))
        elif check_blackjack(args[0].cards) and not check_blackjack(comp.cards):
            pot.pay(args[0], winner='player', typ='blackjack')
            print(args[0].name + " wins with Blackjack over dealer's 21.\nAccount Balance: {}"\
                .format(args[0].balance))
        elif not(check_blackjack(args[0].cards)) and check_blackjack(comp.cards):
            pot.pay(comp, winner='dealer')
            print('Dealer has Blackjack; Player does not. Bet lost.\nNew Account Balance: {}'\
                .format(args[0].balance))
        elif not check_blackjack(args[0].cards) and not check_blackjack(comp.cards):
            pot.pay(args[0], winner='tie')
            print('Tie. Bet returned.\nAccount Balance: {}'.format(args[0].balance))
        return True

    # otherwise, computer wins. pay computer
    else:
        if check_blackjack(comp.cards):
            pot.pay(comp, winner='dealer')
            print('Dealer wins with Blackjack. Bet lost.\nNew Account Balance: {}'\
                .format(args[0].balance))
        else:
            pot.pay(comp, winner='dealer')
            print('Dealer wins. Bet lost.\nNew Account Balance: {}'.format(args[0].balance))
        return True

# initialise required objects
deck = Deck()
pot = Pot()

# ask for the player's name!
name = input('Please Enter Your Name: ')

# Clear outputs
os.system('clear')
clear_output()

# initialise player and dealers
comp = Player('Computer', 10000)
p1 = Player(name, 100)

# play the game!
while True:
    if play_round(comp, p1):
        while True:
            x = input('Another round? [y/n] ').lower()
            if x == 'y' or x == 'n':
                break
        if x == 'n':
            print('Okay. Thanks for playing! Your final balance was {}'.format(p1.balance))
            break

        elif p1.balance == 0:
            print(p1)
            print('Sorry mate, you got no money left.')
            break

        elif x == 'y':

            # Clear outputs
            os.system('clear')
            clear_output()
