#-------------------------------------------------------------------------------
#
#
# Created by Leah Sheptycki
#
# This was an assignment done at the University of Alberta.
# Here is the game of war. For those who've never played it before here are
# the instructions:
#     
#     Two people take half a deck, and flip the top card. Whoevers got the
# highest card wins! If players match cards they call war and lay down 1-3
# cards face down and then flip the last. Whoever succeeds wins all those cards.
# The game ends when one person has no cards left.
#
# To shuffle cards, just use the shuffleCards.py which changes the order in
# shuffledDeck.txt.
#
#
#-------------------------------------------------------------------------------

import random
class Game:
    # Task 1
    
    # Make a game instance
    def __init__(self):
        
        # Suits and face for error checking / ranking,
        # order for face is important.
        self.suits = ['H', 'S', 'C', 'D']
        self.face = ['1', '2', '3', '4', '5', '6', '7', '8',
                     '9', '0', 'J', 'Q', 'K', 'A']  
        self.end_game = False
        
        # Read the deck, that is user inputted
        self.deck = self.read()
        
        # Decide on War Cards
        self.nb_war_cards = int(
            input("Would you like to play war with 1, 2, " +
                  "or 3 cards face-down? "))
        
        # Initialize Players
        self.player_1 = Player()
        self.player_2 = Player()
        
        # Deal cards out, starting with a random player
        self.deal()
        
        # Create the table
        self.cards_on_table = OnTable()
        
        # Start the game loop
        self.play()
        
    def play(self):
        
        # While the game continues...
        while not self.end_game:
            
            # Player 1 plays, and if empty game is over
            face_up_1 = self.player_1.play_card()
            if face_up_1 == 'Empty' or self.player_1.count() == 0:
                print("Player 2 wins")
                self.end_game = True
                break
            
            # Player 2 does the same and if empty game is over
            face_up_2 = self.player_2.play_card()
            if face_up_2 =='Empty' or self.player_2.count() == 0:
                print("Player 1 wins")
                self.end_game = True
                break
            
            # Place both cards face up on the table then print
            self.cards_on_table.place(1, face_up_1, False)
            self.cards_on_table.place(2, face_up_2, False)
            print(self.cards_on_table.__str__())
            print("player_1: " + self.player_1.count())
            print("player_2: " + self.player_2.count())
            input("Press return key to continue\n")
            
            # Compare two cards and decide winner    
            winner = self.compare(face_up_1, face_up_2)
            
            # Player 1 wins, then recieves all cards
            if winner == 1:
                won_cards = self.cards_on_table.cleanTable()
                for card in won_cards:
                    self.player_1.recieve_cards(card)
            
            # Player 2 wins, same thing        
            elif winner == -1:
                won_cards = self.cards_on_table.cleanTable()
                for card in won_cards:
                    self.player_2.recieve_cards(card) 
            
            # If war?        
            else:
                
                # Play amount of cards equal to war cards
                # And then check them if empty, and if so opponent wins
                for i in range(self.nb_war_cards):
                    war_card_1 = self.player_1.play_card()
                    
                    if war_card_1 == 'Empty' or self.player_1.count() == 0:
                        cards_won = self.cards_on_table.cleanTable()
                        self.player_2.recieve_cards(cards_won)
                        print("Player 2 wins!")
                        self.end_game = True
                        break
                    else:    
                        self.cards_on_table.place(1, war_card_1, True)
                    
                    war_card_2 = self.player_2.play_card()
                    if war_card_2 == 'Empty' or self.player_2.count() == 0:
                        cards_won = self.cards_on_table.cleanTable()
                        print("Player 1 wins!")
                        self.player_1.recieve_cards(cards_won)
                        self.end_game = True
                        break
                    else:    
                        self.cards_on_table.place(2, war_card_2, True)
    
        
    # Read the file given, and assure its formatting
    def read(self):
        user = "shuffledDeck.txt"
        try:
            shuffled = open(user, 'r')
            deck = []
            for i in shuffled.readlines():
                # Make sure each card is properly formatted
                i = i[0:2]
                assert len(i) == 2, "Cards not formatted properly."
                assert i[0] in self.face and i[1] in self.suits, "Cards not formatted properly"
                
                # Append to deck if proper
                deck.append(i)
                
            # Make sure the deck has 52 cards
            assert len(deck) == 52, "Not enough cards"
            
        except FileNotFoundError:
            raise Exception('File does not exist')
        return deck
        
    def deal(self):
        
        c_flip = random.randint(0,2)
        for card in self.deck:
            # Coin flip decides whos first, then it alternates
            if c_flip == 1:
                self.player_1.recieve_cards(card)
                c_flip = 0
            else:
                self.player_2.recieve_cards(card)
                c_flip = 1
            
        
    def compare(self, p1, p2):
        # Compares only the first digit/letter based on the index of our
        # face attribute. 0 is war, 1 is p1, -1 is p2
        if self.face.index(p1[0]) == self.face.index(p2[0]):
            return 0
        elif self.face.index(p1[0]) > self.face.index(p2[0]):
            return 1
        elif self.face.index(p1[0]) < self.face.index(p2[0]):
            return -1

# Player Object
class Player:
    
    # Make a queue
    def __init__(self):
        self.pile = CircularQueue(52)
    
    # Recieves dealt or won cards (enqueue)
    def recieve_cards(self, cards):
        self.pile.enqueue(cards) 
    
    # Plays card (dequeue)        
    def play_card(self):
        card = self.pile.dequeue()
        return card
    
    # Returns string of the size
    def count(self):
        return str(self.pile.size())
        
# Table Instance
class OnTable:
    
    # Creates two CircularQueues
    def __init__(self):
        self.__cards = CircularQueue(52)
        self.__faceUp = CircularQueue(52)
    
    # Places a card in one, and then its hidden value in another
    def place(self, player, card, hidden):
        if player == 1:
            self.__cards.insert(card)
            self.__faceUp.insert(hidden)
        elif player == 2:
            self.__cards.enqueue(card)
            self.__faceUp.enqueue(hidden)
    
    # Takes all cards from table, cleans it off, then gives to winner
    def cleanTable(self):
        cards_won = self.__cards.see_all()
        self.__cards.clear()
        self.__faceUp.clear()
        return cards_won
    
    # Returns a string of the containers, and if a card is hidden displays "XX"
    def __str__(self):
        currentList = self.__cards.see_all()
        store = []
        for card in currentList:
            cardIndex = currentList.index(card)
            if self.__faceUp.see_all()[cardIndex]:
                store.append('XX')
            else:
                store.append(card)
        return store
            
        
class CircularQueue:
    def __init__(self, capacity):
        if type(capacity) != int or capacity<=0:
            raise Exception ('Capacity Error')
        self.__items = []
        self.__capacity = capacity
        self.__count=0
        self.__head=0
        self.__tail=0    
        
    def enqueue(self, item):
        
        if self.__count== self.__capacity:
            raise Exception('Error: Queue is full')
        if len(self.__items) < self.__capacity:
            self.__items.append(item)
        else:
            self.__items[self.__tail]=item
        self.__count +=1
        self.__tail=(self.__tail +1) % self.__capacity         

    def dequeue(self):
        if self.__count == 0:
            return "Empty"
        item= self.__items[self.__head]
        self.__items[self.__head]=None
        self.__count -=1
        self.__head=(self.__head+1) % self.__capacity
        return item  
    
    # Insert in the front of the queue
    def insert(self, item):
        
        if self.__count== self.__capacity:
            raise Exception('Error: Queue is full')
        
        if len(self.__items) < self.__capacity:
            self.__items.insert(0, item)
            
        self.__count +=1
        self.__tail=(self.__tail +1) % self.__capacity   
        
    
    def peek(self):
        if self.__count == 0:
            raise Exception('Error: Queue is empty')
        return self.__items[self.__head]
    
    def see_all(self):
        return self.__items
    
    def isEmpty(self):
        return self.__count == 0     
    
    def isFull(self):
        return self.__count == self.__capacity 
    
    def size(self):
        return self.__count     
    
    def capacity(self):
        return self.__capacity    
    
    def clear(self):
        self.__items = []
        self.__count=0
        self.__head=0
        self.__tail=0  
        
    def __str__(self):
        str_exp = "]"
        i=self.__head
        for j in range(self.__count):
            str_exp += str(self.__items[i]) + " "
            i=(i+1) % self.__capacity
        return str_exp + "]"  
        


Game()
            