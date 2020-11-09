#
#    As you may have heard of before, this is the game 2048! It was created as
#    an assignment at the University of Alberta, and you can play the game
#    right here! It even keeps track of your score!
#
#    Made by Leah Sheptycki
#


import random as rnd
import os
import sys
#-------------------[CREATE GRID OBJECT]----------------------------------------
class Grid():
    def __init__(self, row=4, col=4, initial=2):
        self.row = row                              # number of rows in grid
        self.col = col                              # number of columns in grid
        self.initial = initial                      # number of initial cells filled
        self.score = 0

        self._grid = self.createGrid(row, col)      # creates grid specified above

        self.emptiesSet = list(range(row * col))    # list of empty cells

        for _ in range(self.initial):               # assignation to two random cells
            self.assignRandCell(init=True)

#-------------------[CREATE GRID]-----------------------------------------------

    def createGrid(self, row, col):
        
        # Makes the base grid
        grid = []
        
        # For each row
        for row_num in range(row):
            
            # We create a temp list
            temp = []
            
            # and for each column
            for col_num in range(col):
                
                # We append to temp
                temp.append(0)
            
            # and then we append the temp list, to the list of lists
            grid.append(temp)
            
        return grid

#-------------------[SETTING A CELLS VALUE]-------------------------------------

    def setCell(self, cell, val):
        
        # Dividing by 4 and converting to int gets us the row position
        row = int(cell / 4)
        
        # Modulus 4 to find the remainder, which is the column
        col = cell % 4
        
        # Then using those, assign the value
        self._grid[row][col] = val
        
#-------------------[GET CURRENT VALUE FROM CELL]-------------------------------

    def getCell(self, cell):
        
        # Same as above, but instead of assigning it tells values
        row = int(cell / 4)
        col = cell % 4
        return self._grid[row][col]

#-------------------[ASSIGN A NEW VALUE TO A RANDOM CELL]-----------------------

    def assignRandCell(self, init=False):

        """
        This function assigns a random empty cell of the grid
        a value of 2 or 4.

        In __init__() it only assigns cells the value of 2.

        The distribution is set so that 75% of the time the random cell is
        assigned a value of 2 and 25% of the time a random cell is assigned
        a value of 4
        """

        if len(self.emptiesSet):
            cell = rnd.sample(self.emptiesSet, 1)[0]
            if init:
                self.setCell(cell, 2)
            else:
                cdf = rnd.random()
                if cdf > 0.75:
                    self.setCell(cell, 4)
                else:
                    self.setCell(cell, 2)
            self.emptiesSet.remove(cell)

#-------------------[DRAW BOARD STATE]------------------------------------------

    def drawGrid(self):

        """
        This function draws the grid representing the state of the game
        grid
        """

        for i in range(self.row):
            line = '\t|'
            for j in range(self.col):
                if not self.getCell((i * self.row) + j):
                    line += ' '.center(5) + '|'
                else:
                    line += str(self.getCell((i * self.row) + 
                                             j)).center(5) + '|'
            print(line)
        print()

#-------------------[UPDATE EMPTY CELLS]----------------------------------------

    def updateEmptiesSet(self):
        # First make a container
        empties = []
        
        # For each row (4)
        for row_num in range(len(self._grid)):
            
            # and for each column (4)
            for col_num in range(len(self._grid[row_num])):
                
                # We check if it is empty
                if self._grid[row_num][col_num] == 0:
                    
                    # If so, convert into a cell
                    cell = row_num*4+col_num
                    
                    # Append to Container
                    empties.append(cell)
                    
        # Make the container the emptiesSet            
        self.emptiesSet = empties

#-------------------[CHECK IF ROW CAN BE COLLAPSED]-----------------------------

    def collapsible(self):
        
        # For each row...
        for row_num in range(len(self._grid)):
            row = self._grid[row_num]
            
            # If there is a zero, it is collapsable
            if 0 in row:
                return True
            
            # If not, whe check each column and directions for matches
            for col_num in range(len(row)):
                col = self._grid[row_num][col_num]
                
                # Right, Left, Up, Down positions
                # as well as their conditionals
                # and their success conditions
                
                # Checks right
                rightNum = row.index(col) + 1
                if rightNum <= 3:
                    if row[rightNum] == row[col_num]:
                        return True
                
                # Checks left
                leftNum = row.index(col) - 1
                if leftNum >= 0:
                    if row[leftNum] == row[col_num]:
                        return True
                
                # Checks up
                upNum = self._grid.index(row) + 1
                if upNum >= 0:
                    if self._grid[upNum][col_num] == row[col_num]:
                        return True
                    
                # Checks down
                downNum = self._grid.index(row) - 1
                if downNum <= 3:
                    if self._grid[downNum][col_num] == row[col_num]:
                        return True
                    
                
        # if all else fails: False.
        return False
 
 #-------------------[COLLAPSE ROW IN SPECIFIED DIRECTION]----------------------   
            
    def collapseRow(self, lst):
        
        # This is our true or false return to see if changes are made
        moved = False
        
        # First we count towards the length of the list
        # and we add things appropriately
        for num in range(len(lst)):
            
            # This gets the current value of the position in the list
            value = lst[num]
            
            # If it's not the last value (otherwise index error) we continue
            if num < 3:
                one_right = lst[num + 1]
                
                # If the value on the right matches our value,
                # we add the values (doubling has same result) then zero out 2nd
                if one_right == value:
                    lst[num] *= 2
                    lst[num+1] = 0
                    moved = True
                    self.score += lst[num]
                
                # If one_right is zero, we must look further if possible
                elif one_right == 0 and num < 2:
                    two_right = lst[num + 2]
                    
                    # If we find the same value two to the right, we add values
                    # and then zero out the value taken from
                    if two_right == value:
                        lst[num] *= 2
                        lst[num+2] = 0
                        moved = True
                        self.score += lst[num]
                        
                    # And finally, if there is nothing one or two right
                    # we check if the third is not 0, if so it does as follows
                    elif two_right == 0 and num < 1:
                        three_right = lst[num + 3]
                        
                        # If value is not zero, then add and zero out thirdRight
                        if three_right == value:
                            lst[num] *= 2
                            lst[num+3] = 0
                            moved = True 
                            self.score += lst[num]
                            
                            
        # This run is to move values after adding                    
        for num in range(len(lst)):
            
            # This gets the current value of the position
            value = lst[num]
            
            # If it is not the last value, and the value itself is 0
            if num < 3 and value == 0:
                one_right = lst[num + 1]
                
                # If value is zero, but one right is not, switch values.
                # In effect, this will slide left.
                if one_right != 0:
                    lst[num] = lst[num+1]
                    lst[num+1] = 0
                    moved = True
                
                # If one_right is zero, we must look further if possible
                elif one_right == 0 and num < 2:
                    two_right = lst[num + 2]
                        
                    # If value is zero, and two_right is not zero, 
                    # we then switch them. In effect, this will slide left
                    if two_right != 0:
                        lst[num] = lst[num+2]
                        lst[num+2] = 0
                        moved = True
                    
                    # And finally, if there is nothing one or two right
                    # we check if the third is not 0, if so it does as follows
                    elif two_right == 0 and num < 1:
                        three_right = lst[num + 3] 
                            
                        # If the third right value isn't zero, we slide   
                        if three_right != 0:
                            lst[num] = lst[num+3]
                            lst[num+3] = 0
                            moved = True
            
        return lst, moved
 
#-------------------[COLLAPSE ROW UPWARDS]-------------------------------------- 
            
    def collapseLeft(self):
        moved = False
        
        # I chose to cycle through numbers because if I used index then
        # rows could not be duplicate else there is a bug.
        for row_num in range(len(self._grid)):
            
            # Here is the REAL list for the row
            row = self._grid[row_num]
            self._grid[row_num], moved = self.collapseRow(row)
            
            # [BUG FIX] If a row or col was full, moved would be false
            # So if true, moving it to another variable to return keeps it
            if moved == True:
                collapsed = True            

        return collapsed

#-------------------[COLLAPSE ROW RIGHT]----------------------------------------

    def collapseRight(self):
        
        moved = False
        
        # Same as left, but reversed the rows.
        for row_num in range(len(self._grid)):
            
            # Reverse it
            self._grid[row_num].reverse()
            
            # Collapse it
            self._grid[row_num], moved = self.collapseRow(self._grid[row_num])
            
            # and then reversed back.
            self._grid[row_num].reverse()
            
            # [BUG FIX] If a row or col was full, moved would be false
            # So if true, moving it to another variable to return
            if moved == True:
                collapsed = True
                
            
        return collapsed 

#-------------------[COLLAPSE ROW UPWARDS]--------------------------------------

    def collapseUp(self):

        for col_num in range(len(self._grid[0])):
            # Temp storage
            up_list = []
            
            # Add col values to storage
            for row in self._grid:
                up_list.append(row[col_num])
            
            # Collapse list
            up_list, moved = self.collapseRow(up_list)
            
            # Replace Col Values
            i = 0
            for row_num in range(len(self._grid)):
                self._grid[row_num][col_num] = up_list[i]
                i += 1
            
            # [BUG FIX] If a row or col was full, moved would be false
            # So if true, moving it to another variable to return
            if moved == True:
                collapsed = True            
                
        return collapsed

#-------------------[COLLAPSE ROW DOWNWARDS]------------------------------------

    def collapseDown(self):

        # For each column do the following:
        for col_num in range(len(self._grid[0])):
            
            # Make Temporary storage
            down_list = []
            
            # Add col values to storage
            for row in self._grid:
                down_list.append(row[col_num])
            
            # Reverse list   
            down_list.reverse()
            
            # Collapse list
            down_list, moved = self.collapseRow(down_list)
            
            # Unreverse list
            down_list.reverse()
            
            # Replace col values
            i = 0
            for row_num in range(len(self._grid)):
                self._grid[row_num][col_num] = down_list[i]
                i += 1
                
            # [BUG FIX] If a row or col was full, moved would be false
            # So if true, moving it to another variable to return
            if moved == True:
                collapsed = True  
                
        return collapsed

#-------------------[MAIN GAME OBJECT]------------------------------------------

class Game():
    def __init__(self, row=4, col=4, initial=2):

        
        # Creates a game grid and begins the game
        

        self.game = Grid(row, col, initial)
        self.play()

#-------------------[DISPLAY PROMPT]--------------------------------------------

    def printPrompt(self):

        """
        #Prints the instructions and the game grid with a move prompt
        """

        if sys.platform == 'win32':
            os.system("cls")
        else:
            os.system("clear")

        print('Press "w", "a", "s", or "d" to move Up, Left, Down or Right respectively.')
        print('Enter "p" to quit.\n')
        self.game.drawGrid()
        print('\nScore: ' + str(self.game.score))

#-------------------[PLAY LOOP]-------------------------------------------------
        
    def play(self):

        moves = {'w' : 'Up',
                 'a' : 'Left',
                 's' : 'Down',
                 'd' : 'Right'}

        stop = False
        collapsible = True

        while not stop and collapsible:
            self.printPrompt()
            key = input('\nEnter a move: ')

            while not key in list(moves.keys()) + ['p']:
                self.printPrompt()
                key = input('\nEnter a move: ')

            if key == 'p':
                stop = True
            else:
                move = getattr(self.game, 'collapse' + moves[key])
                collapsed = move()

                if collapsed:
                    self.game.updateEmptiesSet()
                    self.game.assignRandCell()

                collapsible = self.game.collapsible()

        if not collapsible:
            if sys.platform == 'win32':
                os.system("cls")
            else:
                os.system("clear")
            print()
            self.game.drawGrid()
            print('\nScore: ' + str(self.game.score))
            print('No more legal moves.')

#-------------------[MAIN FUNCTION CALL]----------------------------------------

def main():
    game = Game()

main()


