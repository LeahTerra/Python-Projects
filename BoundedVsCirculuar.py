#-------------------------------------------------------------------------------
#
#
# Created by Leah Sheptycki
#
# This is just a time comparison between a bounded queue vs a circluar queue
#
#
#-------------------------------------------------------------------------------


import time

class BoundedQueue:
    
    # Constructor, which creates a new empty queue:
    def __init__(self, capacity):
        assert isinstance(capacity, int), ('Error: Type error: %s' % (type(capacity)))
        assert capacity >= 0, ('Error: Illegal capacity: %d' % (capacity))
        self.__items = []
        self.__capacity = capacity
        
    # Adds a new item to the back of the queue, and returns nothing:
    def enqueue(self, item):
        if len(self.__items) >= self.__capacity:
            raise Exception('Error: Queue is full')
        self.__items.append(item)
    
    # Removes and returns the front-most item in the queue.
    # Returns nothing if the queue is empty.
    def dequeue(self):
        if len(self.__items) <= 0:
            raise Exception('Error: Queue is empty')
        return self.__items.pop(0)

    # Returns the front-most item in the queue, and DOES NOT change the queue.
    def peek(self):
        if len(self.__items) <= 0:
            raise Exception('Error: Queue is empty')
        return self.__items[0]
    
    # Returns True if the queue is empty, and False otherwise:
    def isEmpty(self):
        return len(self.__items) == 0

    # Returns True if the queue is full, and False otherwise:
    def isFull(self):
        return len(self.__items) == self.__capacity    
    
    # Returns the number of items in the queue:
    def size(self):
        return len(self.__items)
    
    # Returns the capacity of the queue:
    def capacity(self):
        return self.__capacity    
    
    # Removes all items from the queue, and sets the size to 0
    # clear() should not change the capacity
    def clear(self):
        self.__items = []
        
    # Returns a string representation of the queue:
    def __str__(self):
        str_exp = ""
        for item in self.__items:
            str_exp += (str(item) + " ")
        return str_exp
    
    # Returns a string representation of the object
    # bounded queue:
    def __repr__(self):
        return str(self) + " Max=" + str(self.__capacity)     
        
        
class CircularQueue:
# Constructor, which creates a new empty queue:
    def __init__(self, capacity):
        if type(capacity) != int or capacity<=0:
            raise Exception('Capacity Error')
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
        
    # Removes and returns the front-most item in the queue.
    # Returns nothing if the queue is empty.
    def dequeue(self):
        if self.__count == 0:
            raise Exception('Error: Queue is empty')
        item= self.__items[self.__head]
        self.__items[self.__head]=None
        self.__count -=1
        self.__head=(self.__head+1) % self.__capacity
        return item
    
    # Returns the front-most item in the queue, and DOES NOT change the queue.
    def peek(self):
        if self.__count == 0:
            raise Exception('Error: Queue is empty')
        return self.__items[self.__head]        

    # Returns True if the queue is empty, and False otherwise:
    def isEmpty(self):
        return self.__count == 0
    
    # Returns True if the queue is full, and False otherwise:
    def isFull(self):
        return self.__count == self.__capacity
    
    # Returns the number of items in the queue:
    def size(self):
        return self.__count
    # Returns the capacity of the queue:
    def capacity(self):
        return self.__capacity
    
    # Removes all items from the queue, and sets the size to 0
    # clear() should not change the capacity
    def clear(self):
        self.__items = []
        self.__count=0
        self.__head=0
        self.__tail=0
        
    # Returns a string representation of the queue:
    def __str__(self):
        str_exp = "]"
        i=self.__head
        for j in range(self.__count):
            str_exp += str(self.__items[i]) + " "
            i=(i+1) % self.__capacity
        return str_exp + "]"
    
    # # Returns a string representation of the object CircularQueue
    def __repr__(self):
        return str(self.__items) +  'H=' + str(self.__head) +  'T= '+ str(self.__tail) + '(' +str(self.__count)+"/"+str(self.__capacity)+")"




# WRITTEN CODE STARTS HERE

def boundruntime():
    BQue = BoundedQueue(40)
    for i in range(40):
        BQue.enqueue(i)
    start = time.time()
    for i in range(10000):
        for i in range(0, BQue.size()):
            BQue.dequeue()    
    end = time.time()
    time_interval = end - start
    return(time_interval)

def circleruntime():
    CQue = CircularQueue(40)
    for i in range(40):
        CQue.enqueue(i)    
    start = time.time()
    for i in range(10000):
        for i in range(0, CQue.size()):
            CQue.dequeue()
    end = time.time()
    time_interval = end - start
    return(time_interval)

def run():
    Bound,BCount = [], 0.00
    Circle,CCount = [], 0.00
    
    for i in range(100):
        Bound.append(boundruntime())
        Circle.append(circleruntime())
    for i in range(100):
        BCount += Bound[i]
        CCount += Circle[i]
    BCount = BCount / 100
    CCount = CCount / 100
    
    print("Bound average runtime was: "+ str(BCount))
    print("Circle average runtime was: " + str(CCount))
    
    if BCount < CCount:
        print("Bound wins overall.")
    elif CCount < BCount:
        print("Circle wins overall.")
    else:
        print("Its a tie?")
    
run()