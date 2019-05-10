# This is a Joystick Class which will hold the Joystick Values
import time

class Joystick:

    # Initial setup
    def __init__(self):
        # Detect if the Bat is long
        self._longerBat = False


        #Keeps the number of turns we have had
        self._serves = 0
        
        
        # Keeps score when we win
        self._score = 0

        # Keeps time for how long we have the bat
        self._lengthOfTimeBatUsed = 0.0

        # keeps count of how many times we have used the longer bat option
        self._numberOfLongerBatUsed=0

        # Has the current position of the bat
        self._currentPos = 0

        # Has the previous position of the bat
        self._previousPos = 0

        # previous size of bat
        self._previousLongerBat= False
     
    def getPreviousPosition(self):
        return self._previousPos

    def setBatPosition(self, joystickValue):
        self._previousPos=self._currentPos
        if self._longerBat:
            offset=6
        else:
            offset=3
        self._currentPos=int(joystickValue*(24-offset))

    #return score
    def getScore(self):
        return self._score


    # Get Longer Bat
    def getLongerBat(self):
        return self._longerBat

    # Get Longer Bat
    def getPreviousLongerBat(self):
        return self._previousLongerBat

    # Get serve
    def getServes(self):
        return self._serves

    # Returns Current Position
    def getCurrentPosition(self):
        return self._currentPos



    #set longerbat to boolean parameter
    def setLongerBat(self):
        if (self._numberOfLongerBatUsed<2):
            self._lengthOfTimeBatUsed = time.time()
            self._previousLongerBat=bool(self._longerBat)
            self._longerBat = True

    #set whether this player is serving
    def incSevers(self):
        self._serves += 1

    def update(self):
        if self._longerBat and ((time.time()-self._lengthOfTimeBatUsed)>15.0):
            self._longerBat=False
            self._numberOfLongerBatUsed+=1

    # increments score
    def incScore(self):
        self._score+=1



