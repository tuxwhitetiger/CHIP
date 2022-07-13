from array import *
from enum import Enum
from random import randon as rand


class Direction(Enum):
    UP=0
    DOWN=1
    LEFT=2
    RIGHT=3
    NONE=4


class Head :
    x=0
    y=0
    direction=Direction.RIGHT

class Food :
    x=0
    y=0

class tailSegment :
    x=0
    y=0
    direction=Direction.NONE
    following=None
    moving=False
    startmoving=False

class snake:
    score = 0
    playing =True
    head = Head()
    segments = []
    food = Food()

    def makenewfood(self):
        global food
        food.x = rand.randint(0, 64)
        food.y = rand.randint(0, 32)

    def gameover(self):
        segments.clear()
        playing = False


    def moveseg(self,seg):
        if(seg.moving == True): 
            if(seg.direction == 0): #up
                seg.y -= 1
            elif(seg.direction == 1): #down
                seg.y += 1
            elif(seg.direction == 2): #left
                seg.x -= 1
            elif(seg.direction == 3): #right
                seg.x += 1
            ## update direction after moving
            seg.direction = seg.following.direction
        elif(seg.startmoving):
            seg.moving = True
        elif ((seg.x == seg.following.x) & (seg.y == seg.following.y)) : ## if its at the end of the tail start moving
            seg.startmoving = True
        
    def movehead(self):
        global head
        # death on wall colition logic needs adding .... this needs to be on head logic 
        if(head.direction == 0): #up
            head.y -= 1
        elif(head.direction == 1): #down
            head.y += 1
        elif(head.direction == 2): #left
            head.x -= 1
        elif(head.direction == 3): #right
            head.x += 1

        #cheack for wall colition
        if(head.y == 0):
            #death
            gameover(self)
        elif(head.y == 32):
            #death
            gameover(self)
        elif(head.x == 0):
            #death
            gameover(self)
        elif(head.x == 64):
            #death
            gameover(self)

    def foodcheck(self) :
        global score
        global head
        global segments
        global food
        if ((head.x == food.x) & (head.y == food.y)):
            makenewfood(self)
            score = score + 1
            newtail = tailSegment()
            newtail.x = head.x
            newtail.y = head.y
            newtail.direction = head.direction
            newtail.following = segments.index(segments.count()-1)
            segments.append(newtail)


    ##setup
    def setup(self):
        global score
        global head
        global segments
        global food
        score = 0
        playing =True
        head = Head()
        segments = []
        food = Food()
        ##setup head
        head.x = 8
        head.y = 16
        head.direction = Direction.LEFT
        ##setup food
        self.makenewfood()
        ##setup start of tail
        newtail = tailSegment()
        newtail.x = head.x-1
        newtail.y = head.y
        newtail.direction = head.direction
        newtail.following = segments.index(segments.count()-1)
        segments.append(newtail)

        score = 0


    ##update loop
    def update(self):
        ##check for controller input
        ##for now randomize direction
        global head
        head.direction = rand.randint(0, 3)

        global segments
        foodcheck(self)
        movehead(self)
        for seg in segments:
            moveseg(self,seg)
        
