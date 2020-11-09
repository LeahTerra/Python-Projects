import sqlite3
import datetime as d
from pathlib import Path
from mp1 import *

# Our main function!
def search_rides(email, connection, cursor):
    
    keywords = ['','','']
    keys = input("What are your 1-3 keywords for the search?: ").split()
    
    for i in range(0, len(keys)):
        keywords[i] = keys[i]
        globalInputCheck(keywords[i])
    
    if(0 < len(keywords) < 4):
        pass
    else:
        print("Error in Keywords")
        search_rides(email, connection, cursor)
	
    rides = getMatches(keywords, connection, cursor)
    if len(rides) == 0:
        print("No results.")
        search_rides(email, connection, cursor)
        
    rides = list(makePages(rides))
    menuDone = menu(rides, 0)
    if menuDone == 0:
        search_rides(email, connection, cursor)    
    elif menuDone == 1:
        sendMessage(email, connection, cursor)
        menu(rides, 0)
    elif menuDone == 2:
        return
    
# Gets all results matching keyword, if more than one it concatinates the sql query
def getMatches(keywords, connection, cursor):
    
    checkRides = '''
            SELECT r.rno, r.price, r.rdate, r.seats, r.lugDesc, r.src, r.dst, r.driver, c1.make, c1.model, c1.year
            FROM   rides r
                INNER JOIN (select c.cno, c.make, c.model, c.year, c.seats, c.owner from cars c) c1 on c1.cno = r.cno
            WHERE  r.src = :KW1
            OR r.dst = :KW1
            OR r.rno IN (SELECT e.rno
			 FROM   enroute e
			 WHERE  e.rno = r.rno
			 AND e.lcode = :KW1)

            OR r.src IN (SELECT l.lcode
			 FROM   locations l
			 WHERE  l.city LIKE :KW1L
			 OR l.address LIKE :KW1L
			 OR l.prov LIKE :KW1L
			   AND r.src = l.lcode)
			 
            OR r.dst IN (SELECT l.lcode
			 FROM   locations l
			 WHERE  l.city LIKE :KW1L
			 OR l.address LIKE :KW1L
			 OR l.prov LIKE :KW1L
			   AND r.dst = l.lcode)
            '''
    checkR2 = '''
            INTERSECT
            SELECT r.rno, r.price, r.rdate, r.seats, r.lugDesc, r.src, r.dst, r.driver, c1.make, c1.model, c1.year
            FROM   rides r
                INNER JOIN (select c.cno, c.make, c.model, c.year, c.seats, c.owner from cars c) c1 on c1.cno = r.cno
            WHERE  r.src = :KW2
            OR r.dst = :KW2
            OR r.rno IN (SELECT e.rno
			 FROM   enroute e
			 WHERE  e.rno = r.rno
			 AND e.lcode = :KW2)

            OR r.src IN (SELECT l.lcode
			 FROM   locations l
			 WHERE  l.city LIKE :KW2L
			 OR l.address LIKE :KW2L
			 OR l.prov LIKE :KW2L
			   AND r.src = l.lcode)
			 
            OR r.dst IN (SELECT l.lcode
			 FROM   locations l
			 WHERE  l.city LIKE :KW2L
			 OR l.address LIKE :KW2L
			 OR l.prov LIKE :KW2L
			   AND r.dst = l.lcode)
                           
            '''
    checkR3 = '''
            INTERSECT
            SELECT r.rno, r.price, r.rdate, r.seats, r.lugDesc, r.src, r.dst, r.driver, c1.make, c1.model, c1.year
            FROM   rides r
                   INNER JOIN (select c.cno, c.make, c.model, c.year, c.seats, c.owner from cars c) c1 on c1.cno = r.cno
            WHERE  r.src = :KW3
            OR r.dst = :KW3
            OR r.rno IN (SELECT e.rno
			 FROM   enroute e
			 WHERE  e.rno = r.rno
			 AND e.lcode = :KW3)

            OR r.src IN (SELECT l.lcode
			 FROM   locations l
			 WHERE  l.city LIKE :KW3L
			 OR l.address LIKE :KW3L
			 OR l.prov LIKE :KW3L
			   AND r.src = l.lcode)
			 
            OR r.dst IN (SELECT l.lcode
			 FROM   locations l
			 WHERE  l.city LIKE :KW3L
			 OR l.address LIKE :KW3L
			 OR l.prov LIKE :KW3L
			   AND r.dst = l.lcode)
            '''
    
    if keywords[1] != '' and keywords[2] == '':
        checkRides += checkR2
    
    elif keywords[2] != '':
        checkRides += checkR2
        checkRides += checkR3
    
    cursor.execute(checkRides, {'KW1': keywords[0], 'KW1L': '%'+keywords[0]+'%','KW2': keywords[1], 'KW2L': '%'+keywords[1]+'%', 'KW3': keywords[2], 'KW3L': '%'+keywords[2]+'%'})
    
    rides= cursor.fetchall()
    return rides

# Here is where the menu directly after you search is, calls itself until given a return code
def menu(rides, index):
    global connection, cursor, email
    printRides(rides[index])
    print('\n')
    
    option1 = 'What would you like to do? (1) Message driver (4) Search Again (5) Go back to menu\nYou can also type /logout to log out or /exit to quit.\n'
    option2 = 'What would you like to do?: (1) Message driver (2) See next page (4) Search Again (5) Go back to menu\nYou can also type /logout to log out or /exit to quit.\n'
    option3 = 'What would you like to do?: (1) Message driver (2) See next page (3) Go back a page (4) Search Again (5) Go back to menu\nYou can also type /logout to log out or /exit to quit.\n'
    option4 = 'What would you like to do?: (1) Message driver (3) Go back a page (4) Search Again (5) Go back to menu\nYou can also type /logout to log out or /exit to quit.\n'
         
    if len(rides) == 1:
        choice = input(option1)
        options = ['1','4','5']
    elif index == 0 and len(rides) > 1:
        choice = input(option2)
        options = ['1', '2','4','5']
    elif index != 0 and index < len(rides)-1:
        choice = input(option3)
        options = ['1','2','3','4','5']
    elif index == len(rides)-1:
        choice = input(option4)
        options = ['1','3','4','5']
    
    globalInputCheck(choice)
    if choice not in options:
        print("Error: Please select one of the options given\n")
        exitCode = menu(rides, index)
    elif choice == '1':
        return 1
    elif choice == '2':
        index+=1
        exitCode = menu(rides, index)
    elif choice == '3':
        index-=1
        exitCode = menu(rides, index)
    elif choice == '4':
        return 0
    elif choice == '5':
        return 2
    
    if exitCode == 0:
        return 0
    elif exitCode == 1:
        return 1
    elif exitCode == 2:
        return 2

# Check whether to logout or exit
def globalInputCheck(word):
        
    if(word == "/exit"):
        exit()
    elif(word == "/logout"):
        logout()

# Prints a formatted table      
def printRides(rides):
    dashes = "-" * 120
    for i in range(0, len(rides)+1):
        if i == 0:
            print(dashes)
            print('{:<9s}{:<8s}{:<13s}{:<8s}{:<15s}{:<8s}{:<8s}{:<20s}{:<12s}{:<10s}{:<6s}'.format('Ride No.', 'Price', 'Ride Date', 'Seats', 'LuggageDesc','Source',' Dest.', 'Driver', 'Make', 'Model', 'Year'))
            print(dashes)
        else:
            print('{:<9d}{:<8d}{:<13s}{:<8d}{:<15s}{:<8s}{:<8s}{:<20s}{:<12s}{:<10s}{:<6d}'.format(rides[i-1][0],rides[i-1][1],rides[i-1][2],rides[i-1][3],rides[i-1][4],rides[i-1][5],rides[i-1][6],rides[i-1][7],rides[i-1][8],rides[i-1][9],rides[i-1][10]))

# This one just splits the data into 'pages'
def makePages(rides):
    pages = []
    for i in range(0, len(rides), 5):
        yield rides[i:i+5]
        
# This function is true to its name, gets info neccisary to insert into messages
def sendMessage(email, connection, cursor):
    rno = input("What is the rno of the driver you'd like to contact?:\n")
    globalInputCheck(rno)
    cursor.execute("SELECT r.driver FROM rides r WHERE r.rno = ?", (rno,))
    driveremail = cursor.fetchone()
    if driveremail == None or len(driveremail) == 0:
        print("Invalid Ride Number");
        sendMessage(email, connection, cursor);
        
    message = input("Enter your message:\n\n")
    globalInputCheck(message)
    
    fullMessage = (driveremail[0], d.datetime.now(), email, message, rno, 'n')

    cursor.execute("INSERT INTO inbox VALUES(?,?,?,?,?,?)", fullMessage)
    connection.commit()
    
    print('Message successfully sent!\n ')
    

        
    