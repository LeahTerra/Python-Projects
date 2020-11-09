#
#    This is the classic game of guessing between 1 and 100, but with a small
#    twist where the computer can be the one guessing using a simple alogrithm
#    Enjoy :)
#
#    Made by Leah Sheptycki
#

import random as rnd

#----------------------[PLAYER IS GUESSING]-------------------------------------
class Game1:
    
    def __init__(self):
        # Game Breakers.
        self.keep_going = True
        self.won = False
        
        # Creates a player guessable number and defines guesses.
        self.rand_num = rnd.randint(0,101)
        self.guesses = 6
        self.game()
        
    def game(self):
        
        # While game is active, print standard greeting, check guess,
        # then check if game should continue.
        while self.keep_going:
            
            guess = input("Your Guess: ")
            if guess == 'exit':
                self.keep_going = False
                break
            
            self.check_guess(int(guess))
            self.check_continue()
            
    def check_guess(self, guess):
        
        # If high or low, say it and reduce a guess. If win, say it and update.
        if guess > self.rand_num:
            print("Too High! \n")
            self.guesses -= 1
        elif guess < self.rand_num:
            print("Too low! \n")
            self.guesses -= 1
        elif guess == self.rand_num:
            print("Hooray you won!")
            self.won = True
            
    def check_continue(self):
        # If the game is won, or player is out of guesses, then the game breaks.
        if self.won == True:
            print("You had " + str(self.guesses) + " guess remaining.")
            self.keep_going = False
        
        elif self.guesses == 0:
            print("Oh no you've lost, the correct number is: "+ 
                  str(self.rand_num))
            self.keep_going = False
   
#----------------------[COMPUTER IS PLAYING]------------------------------------
class Game2:
    
    def __init__(self):
        
        # Win loss conditions
        self.keep_going = True
        self.win = False
        self.guesses = 6
        
        self.A = []
        self.L = 0
        self.R = 100
        self.M = 0
        
        for i in range(0, 101):
            self.A.append(i)
            
        self.game()
        
    def game(self):
        
        while self.keep_going:
            self.comp_guess()
            self.check_continue()
    
    def comp_guess(self):
            
        self.M = (self.L + self.R) // 2
        print("Computer Guess: " + str(self.M) + 
              "  (+ for higher, - for lower, 'win' if it guesses correctly)")
        high_low = input()
        
        # If lower, then the highest number is one less than the current guess
        if high_low == "-":
            self.R = self.M - 1
            self.guesses -= 1
        
        # If higher, then the lowest number is one higher than the current guess   
        elif high_low == "+":
            self.L = self.M + 1
            self.guesses = self.guesses - 1
        
        # Win Condition    
        elif high_low == "win":
            self.win = True
        
        # Exit    
        elif high_low == "exit":
            print("Exitting")
            self.keep_going = False
                
    def check_continue(self):
        
        if self.win == True:
            self.keep_going = False
            print("Yay computer won")
            
        if self.guesses == 0:
            print("Computer is out of guesses")
            self.keep_going = False
        
    
#----------------------[MAIN]---------------------------------------------------
def main():
    player = input("User or Computer?: ")
    if player.lower() == "user":
        Game1()
    elif player.lower() == "computer":
        Game2()
    
main()

            
            
                
        
    