# Constants 
class Constants:
    def __init__(self):
        self._randomSpeed = False
        self._hardware_sound = True
        self._software_sound = False

    #Getter for random speed
    def getRandomSpeed(self):
        return self._randomSpeed

    def is_hardware_sound(self):
        return self._hardware_sound

    def is_software_sound(self):
        return self._software_sound