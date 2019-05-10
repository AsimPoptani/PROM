import time , random
class Ball:

    def __init__(self):
        #Keeps track of where the ball is
        self.ballLocation=[0,0]
        # Keeps track of where the ball was
        self.oldBallLocation=[0,0]

        #Keeps track of velocitys in terms of time
        # North  East  these can be negative
        self.velocitys=[0,0]

        # This tracks how long it has been
        self.timeSpentX=0
        self.timeSpentY=0

    #Tracks if we should use random speed
    def setRandomSpeed(self,enable,nDirection):
        nDirection=  1.0 if nDirection else -1.0
        if (enable):
            self.velocitys=[(random.randint(1,3)/100.0)*nDirection,(random.randint(1,3)/100.0)*random.choice([-1.0,1.0])]
        else:
            self.velocitys=[0.0375*nDirection,0]
        #print(self.velocitys)
        self.timeSpentX=time.time()
        self.timeSpentY=time.time()
    #Allow to set East Velocity
    def setEastVelocity(self,eastVelocity):
        self.velocitys=[self.velocitys[0],eastVelocity]

    #Allow to set North Velocity
    def setNorthVelocity(self,northVelocity):
        self.velocitys=[northVelocity,self.velocitys[1]]

    #returns ball location
    def getBallLocation(self):
        return self.ballLocation

    #returns old ball location
    def getOldBallLocation(self):
        return self.oldBallLocation

    #Update Ball location
    def update(self):
        #Get time diffrence between now and before
        timeDiffrenceX= time.time()-self.timeSpentX
        timeDiffrenceY= time.time()-self.timeSpentY
        newNorthDistanceGained=0
        newSouthDistanceGained=0
        #Calculate distance travelled
        if not self.velocitys[0]==0:
            newNorthDistanceGained=int(timeDiffrenceX/self.velocitys[0])
            #print(timeDiffrenceX)
            if not newNorthDistanceGained==0:
                pass
                #print(newNorthDistanceGained)
        if not self.velocitys[1]==0:
            newSouthDistanceGained=int(timeDiffrenceY/self.velocitys[1])


        #If the distance is significant then we update position
        if abs(newNorthDistanceGained)>=1 or abs(newSouthDistanceGained)>=1:
            potentiialBallLocation=[x + y for x, y in zip(self.ballLocation, [newNorthDistanceGained,newSouthDistanceGained])]
            #Swap velocitys and update!
            if (potentiialBallLocation[1]>22 or potentiialBallLocation[1]<1 ):
                self.velocitys[1]=-self.velocitys[1]
                self.update()
            else:
                # Set the timer going
                if abs(newNorthDistanceGained)>=1:
                    self.timeSpentX=time.time()
                if abs(newSouthDistanceGained)>=1:
                    self.timeSpentY=time.time()
                # Copy the array to the old ball location
                self.oldBallLocation=self.ballLocation.copy()
                # Set the new location
                self.ballLocation=potentiialBallLocation

    #Sets location
    def setLocation(self,x,y):
        # Copy the array to the old ball location
        self.oldBallLocation=self.ballLocation.copy()
        # Set the new location
        self.ballLocation=[x,y]

    def getVelocity(self):
        return self.velocitys
