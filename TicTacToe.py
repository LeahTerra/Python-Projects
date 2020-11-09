#-------------------------------------------------------------------------------
#
#
# Created by Leah Sheptycki
#
# Tic-Tac-Toe! Just follow the prompts and have fun :)
#
#
#-------------------------------------------------------------------------------

class TicTacToe:
    def __init__(self):
        # "board" is a list of 10 strings representing the board (ignore index 0)
        self.board = [" "]*10
        self.board[0]="#"
        
#------------------------------------------------------------- 
    def drawBoard(self):
    # This method prints out the board with current plays adjacent to a board with index.
        levels = [" \t 7 | 8 | 9 \n", " \t 4 | 5 | 6 \n"," \t 1 | 2 | 3 \n", "-----------       -----------"]
        form = [' ', ' | ', '\t']
        print(form[0]+self.board[7]+form[1]+self.board[8]+form[1]+self.board[9]+levels[0]+levels[3])
        print(form[0]+self.board[4]+form[1]+self.board[5]+form[1]+self.board[6]+levels[1]+levels[3])
        print(form[0]+self.board[1]+form[1]+self.board[2]+form[1]+self.board[3]+levels[2])

#------------------------------------------------------------- 
    def boardFull(self):
    # This method checks if the board is already full and returns True. Returns false otherwise
        if ' ' in self.board:
            return False
        else:
            return True

#------------------------------------------------------------- 
    def cellIsEmpty(self, cell):
        
        try:
            if self.board[cell] == ' ':
                return True
            else:
                return False
        except:
            return False

#------------------------------------------------------------- 
    def assignMove(self, cell,ch):
    # assigns the cell of the board to the character ch
        self.board[cell] = ch
        TicTacToe.drawBoard(self)

#------------------------------------------------------------- 
    def whoWon(self):
    # returns the symbol of the player who won if there is a winner, otherwise it returns an empty string. 
        if self.isWinner("x") == True:
            return "x"
        elif self.isWinner("o") == True:
            return "o"
        else:
            return ""

#-------------------------------------------------------------   
    def isWinner(self, ch):
    # Given a player's letter, this method returns True if that player has won.
        result = []
        # This is all winning combinations f
        win_comb = [[1,2,3],[1,4,7],[1,5,9],[2,5,8],[3,6,9],[3,5,7],[4,5,6],[6,8,9]]
        offset = -1
        x = True
        while x == True:
            try:
                offset = self.board.index(ch, offset+1)
                result.append(offset)
            except:
                x = False
        
        for i in win_comb:
            if i[0] in result and i[1] in result and i[2] in result:
                return True

class Game():            
    def gameLoop():
        myBoard=TicTacToe()
        player1 = 'x'
        player2 = 'o'
        loop = True
        playcount = 0
        myBoard.drawBoard()
        while loop == True:
            playcount += 1
            if playcount % 2 == 0:
                currentPlayer = player2
            else:
                currentPlayer = player1
                
            Game.gameMove(myBoard, currentPlayer)
            winner = myBoard.whoWon()
            print(winner)
            if winner == 'x':
                print(winner, 'wins. Congrats!')
                break
                
            elif winner == 'o':
                print(winner, 'wins. Congrats!')
                i = 9
                break
                
            if myBoard.boardFull() == True:
                print("It's a tie.")
                break
                        
    def gameMove(myBoard, player):
        
        move = int(input("It is the turn for "+player+". What is your move? "))
        x = True
        
        while x == True:
            if myBoard.cellIsEmpty(move) == False:
                move = int(input("That space is already taken. Please pick a new cell. "))
            elif move > 9:
                move = int(input("You must pick between 1 and 9. Please pick a new cell. "))
            else:
                myBoard.assignMove(move, player)
                x = False
            
Game.gameLoop()