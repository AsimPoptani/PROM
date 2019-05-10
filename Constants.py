# Constants 
class Constants:
    def __init__(self):
        self._randomSpeed = False
        self._hardware_sound = True

    #Getter for random speed
    def getRandomSpeed(self):
        return self._randomSpeed

    def is_hardware_sound(self):
        return self._hardware_sound