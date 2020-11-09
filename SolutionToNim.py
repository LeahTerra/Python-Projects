# 
#    So this is minimax, a solution to the game of nim. The game of nim is
#    simple strategy game where two players (min and max in this case) must 
#    divide the remaining objects using two different numbers until somebody 
#    cannot do more.
#
#    This program calculates every single possible outcome that could happen
#    using recursive methods. Enjoy it, but I suggest not going over 12 unless 
#    you've got a powerful computer due to the exponential nature of the program.
#
#    This is made by Leah Sheptycki
#
#------------------| MINMAX |--------------------------------------------------|

class Minimax:
    # Here we initialize the object
    def __init__(self, nimState, minMaxLevel):
        self.state = nimState
        self.level = minMaxLevel
        self.child = []
    
    
    def spliter(self, pile):
        # Create blank pile
        new_pile = []
        
        # To go through any possible combinations, we use two increments.
        for i in range(int(pile)):
            for j in range(int(pile)):
                
                # If they add to equal the pile size, they are not identical
                # and if they aren't already there in reverse order:
                if (i + j) == int(pile) and (i is not j) and ([j, i] 
                                                              not in new_pile):
                    
                    # We then add the combination of i and j
                    new_pile.append([i,j])
        
        # Then we return the list of all possible combinations
        return new_pile
    
#------------------| MINMAX |--------------------------------------------------| 
#------------------------- \-> | NEW CHILD |-----------------------------------|

    # If it hits leaf-node, it will not create a new child, 
    # and then return the node    
    def add_child(self, newstate):
        
        # If Max, next level is min.
        if self.level == 'Max':
            new_child = Minimax(newstate, 'Min')
            build(new_child)
        # If min, next level is max.
        else:
            new_child = Minimax(newstate, 'Max')
            build(new_child)
        
        # Add child to the list.
        self.child.append(new_child)
        
#------------------| MINMAX |--------------------------------------------------| 
#------------------------- \-> | PRINTING THE TREE |---------------------------|

    def print_tree(self, indentation, last):
        
        # If its the last in a set of children
        if last:
            
            # Print the indent size, and the proper characters, as well as the
            # state and level, then add space to move indent over
            print(indentation[:-1], '\-', self.state, self.level)
            indentation += "     "
        
        # If there are more children to go, print indent, proper character
        # and the state. Then add line to signify there is more in the tree
        else:
            print(indentation[:-1], "+ ", self.state)
            indentation += "|   "
        
        # For each kid, we do the same as above.
        for kid in self.child:
            
            # If no more kiddos
            if self.child.index(kid) == len(self.child)-1:
                last = True
            else:
                last = False
            kid.print_tree(indentation, last)
            
#-----------------| MAIN FUNCTION |--------------------------------------------|           
def main():
    
    # Try loop to contain error, and while loop to give opportunity to fix error
    while True:
        try:
            user = int(input("Choose your initial size of "+
                             "the pile. Should be more than 2: "))
            if int(user) > 2:
                break
        except ValueError:
            pass
    
    # Build the node with users amount on the stack
    root = Minimax([user], "Max")
    
    # Build the root, which builds everything else
    build(root)
    
    # Call the print function to print tree in proper format
    root.print_tree('', True)
    
#-----------------| BUILDING THE TREE |----------------------------------------|

def build(node):
    
    # For each pile in state
    for k in node.state:
        
        # If it can be split (>2)
        if k > 2:
            
            # Split it into all combinations
            
            possibilities = node.spliter(k)
            
            # Then create new child for each combination
            for possible in possibilities:
                
                # Creates and updates the state for the child
                newstate = []
                
                # This is specifically here to make sure we dont change the
                # original objects attribute
                for i in node.state:
                    newstate.append(i)
                
                # Add the combination to the state and sort
                newstate[-1] = possible[0]
                newstate.append(possible[1])
                newstate.sort()
                
                # Then we make more babies until it cannot make more
                node.add_child(newstate)

#-----------------| FUNCTION CALL |--------------------------------------------| 

main()
    
    