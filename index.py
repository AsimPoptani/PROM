from Game.Screen import Screen
from Game.Joystick import Joystick
from Game.Ball import Ball
from IO.SensorHandler import SensorHandler
from IO.TestSensorHandler import TestSensorHandler
from Constants import Constants
from enum import Enum
from IO.writeOutputs import OutputHandler
import Diagnostics
######## GAME FUNCTIONS #########

# Update all sensors
def updateSensors():
    # Run Diagnostics
    Diagnostics.updateDiagnostic()
    #update sensor handler
    sensorHandler.update()
    #update both joystick position
    joystick1.setBatPosition(sensorHandler.get_knob_A()/0.97)
    joystick2.setBatPosition(sensorHandler.get_knob_B())

def clearBats():
    # Remove Previous bat position
    if (joystick1.getPreviousLongerBat()):
        for sizeOfBat in range(0,6):
            gameScreen.setColourAtLocation(1,joystick1.getPreviousPosition()+sizeOfBat,"Black")
    else:
        for sizeOfBat in range(0,3):
            gameScreen.setColourAtLocation(1,joystick1.getPreviousPosition()+sizeOfBat,"Black")

    if (joystick2.getPreviousLongerBat()):
        for sizeOfBat in range(0,6):
            gameScreen.setColourAtLocation(80,joystick2.getPreviousPosition()+sizeOfBat,"Black")
    else:
        for sizeOfBat in range(0,3):
            gameScreen.setColourAtLocation(80,joystick2.getPreviousPosition()+sizeOfBat,"Black")

# Draws Bats
def drawBats():

    # Add new Bat position
    if (joystick1.getLongerBat()):
        for sizeOfBat in range(0,6):
            gameScreen.setColourAtLocation(1,joystick1.getCurrentPosition()+sizeOfBat,"Red") # Player 1 has a red Joystick
    else:
        for sizeOfBat in range(0,3):

            gameScreen.setColourAtLocation(1,joystick1.getCurrentPosition()+sizeOfBat,"Red") # Player 1 has a red Joystick

    if (joystick2.getLongerBat()):
        for sizeOfBat in range(0,6):
            gameScreen.setColourAtLocation(80,joystick2.getCurrentPosition()+sizeOfBat,"Blue") # Player 2 has a Blue Joystick
    else:
        for sizeOfBat in range(0,3):
            gameScreen.setColourAtLocation(80,joystick2.getCurrentPosition()+sizeOfBat,"Blue") # Player 2 has a Blue Joystick
    # Check if longer Bat pressed
    if (sensorHandler.get_switch_A2()):
        joystick1.setLongerBat()
    if (sensorHandler.get_switch_B2()):
        joystick2.setLongerBat()


# Draws the ball
def drawBall():
    if gameState==GAME_STATES.GAME_PLAYER_ONE_SERVE:
        if (joystick1.getLongerBat()):
            ball.setLocation(2,joystick1.getCurrentPosition()+2)
        else:
            ball.setLocation(2,joystick1.getCurrentPosition()+1)

    elif gameState==GAME_STATES.GAME_PLAYER_TWO_SERVE:
        if (joystick1.getLongerBat()):
            ball.setLocation(79,joystick2.getCurrentPosition()+2)
        else:
            ball.setLocation(79,joystick2.getCurrentPosition()+1)
    elif gameState==GAME_STATES.GAME_START:
        ball.update()
    ballLocation=ball.getBallLocation()
    gameScreen.setColourAtLocation(ballLocation[0],ballLocation[1],"Cyan")

def clearOldBallLocation():
    oldBallLocation=ball.getOldBallLocation()
    gameScreen.setColourAtLocation(oldBallLocation[0],oldBallLocation[1],"Black")


#draws everything
def drawEverything():

    #Clear all the old crap
    clearOldScore()
    clearOldBallLocation()
    clearBats()

    #Draws the bats
    drawBats()
    
    # Draws the net
    drawNet()

    # Draws the score
    drawScore()

    #Draws the ball
    drawBall()



# Draws the net
def drawNet():
    for index in range(6):
        gameScreen.setColourAtLocation(40, (index * 4)+1,"Green")
        gameScreen.setColourAtLocation(40, (index * 4)+2,"Green")

def drawSingleScore(xShift,score,colour="BrightYellow"):
    numberPartRowCounter=0
    for numberPartRow in gameScreen.numbers.get(str(score)):
        numberPartCounter=0
        for numberPart in numberPartRow:
            if (numberPart=="#"):
                gameScreen.setColourAtLocation(xShift+numberPartCounter,numberPartRowCounter,colour)
            numberPartCounter+=1
        numberPartRowCounter+=1

def clearOldScore():
    drawSingleScore(33,'clear',"Black")
    drawSingleScore(45,'clear',"Black")

# Draws the score
def drawScore():
    player1Score = joystick1.getScore()
    player2Score = joystick2.getScore()
    drawSingleScore(33,player1Score)
    drawSingleScore(45,player2Score)




###### GAME STATE #####
# Game states
class GAME_STATES(Enum):
    GAME_INIT = -1
    GAME_START = 0
    GAME_PLAYER_ONE_SERVE=1
    GAME_PLAYER_TWO_SERVE=2
OutputHandler
gameState=GAME_STATES.GAME_INIT
######## INIT #########

#init Screen
gameScreen=Screen()

#init output handler
outputHandler=OutputHandler()

#init constants
constants=Constants()

#init Joysticks
joystick1=Joystick()
joystick2=Joystick()

#init Ball
ball=Ball()

#init Sensor handler
sensorHandler=SensorHandler()
#sensorHandler= TestSensorHandler()

#Update sensors
sensorHandler.update()
drawEverything()
#Update the screen
gameScreen.update()
gameState= GAME_STATES.GAME_PLAYER_ONE_SERVE
while True:
    #update joysticks
    joystick1.update()
    joystick2.update()

    #Update sensors
    updateSensors()

    drawEverything()

    if (gameState==GAME_STATES.GAME_PLAYER_ONE_SERVE):
        if (sensorHandler.get_switch_A1()):
            joystick1.incSevers()
            ball.setRandomSpeed(constants.getRandomSpeed(),True)
            gameState=GAME_STATES.GAME_START

    elif (gameState==GAME_STATES.GAME_PLAYER_TWO_SERVE):
        if (sensorHandler.get_switch_B1()):
            joystick2.incSevers()
            ball.setRandomSpeed(constants.getRandomSpeed(),True)
            gameState=GAME_STATES.GAME_START

    elif(gameState==GAME_STATES.GAME_START):
        #If ball is about to hit the wall detect if paddle is there and if it is calculate

        #get current ball location
        currentBallLocation=ball.getBallLocation
        #Check if its near player 1  and heading in that direction
        if (ball.getBallLocation()[0]==2 and ball.getVelocity()[0]<0):
            sizeOfBat=6 if joystick1.getLongerBat() else 3
            if ball.getBallLocation()[1] in range(joystick1.getCurrentPosition(),joystick1.getCurrentPosition()+sizeOfBat):
                ball.setRandomSpeed(True,True) # Todo need to change

            else:
                joystick2.incScore()
                gameState= GAME_STATES.GAME_PLAYER_TWO_SERVE # Todo need to change

        #Check if its near player 2  and heading in that direction
        elif (ball.getBallLocation()[0]==79 and ball.getVelocity()[0]>0):
            sizeOfBat=6 if joystick2.getLongerBat() else 3
            if ball.getBallLocation()[1] in range(joystick2.getCurrentPosition(),joystick2.getCurrentPosition()+sizeOfBat):
                ball.setRandomSpeed(True,False) # Todo need to change

            else:
                joystick1.incScore()
                gameState= GAME_STATES.GAME_PLAYER_ONE_SERVE # Todo need to change
        
        if (joystick1.getScore()==10):
            outputHandler.piglow_win()
            gameScreen.serialPort.write((gameScreen.ESC+"2J").encode("utf-8"))
            gameScreen._cursorTo(0,12)
            gameScreen.serialPort.write(("--Congrats Left Has Won--").encode("utf-8"))
            exit()
        
        elif (joystick2.getScore()==10):
            outputHandler.piglow_win()
            gameScreen.serialPort.write((gameScreen.ESC+"2J").encode("utf-8"))
            gameScreen._cursorTo(0,12)
            gameScreen.serialPort.write(("--Congrats Right Has Won--").encode("utf-8"))
            exit()            

    # updates the game
    gameScreen.update()
