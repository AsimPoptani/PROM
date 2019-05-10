import smbus
import time
from IO.PyGlow import PyGlow
import RPi.GPIO as GPIO

EXTERNAL_LED_ADDR = 0x3a
SOUND_ADDR = 0x20
BLIP_LENGTH = 20

class OutputHandler():

    def __init__(self):
        self.led_table = [5, 6, 12, 13, 16, 19, 20, 26]
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        for i in self.led_table:
            GPIO.setup(i, GPIO.OUT)

        self._bus = smbus.SMBus(1)
        self._blip_timer = 0
        self._blip_state = False

    def update(self):
        if self._blip_state:
            if self._blip_timer == 0:
                self._bus.write_byte( SOUND_ADDR, 0xff)
                self._blip_state = False
            else:
                self._blip_timer -= 1

    def progressBar(self,progressStage):
        self.set_leds(progressStage,True)

    def set_leds(self, id, state):
        try:
            self._set_pi_leds(id, state)
            self._set_out_leds(id, state)
        except Exception:
            pass

    def _set_pi_leds(self, id, state):
        for i in self.led_table:
            GPIO.output( i, False)
        GPIO.output(self.led_table[id], state)

    def _set_out_leds(self, id, state):
        self.out_led_table = [3,2,1,0,4,5,6,7]
        out = [1 for i in range(8)]
        if not state:
            self._bus.write_byte( EXTERNAL_LED_ADDR, 0xff)
            # print("Switching off", id)
        else:
            out[self.out_led_table[id]] = 0
            stringToBulid=""
            for o in out:
                stringToBulid+= str(o)

            # print(int(stringToBulid,2))
            self._bus.write_byte( EXTERNAL_LED_ADDR, int(stringToBulid,2))
        '''
        for i in range(8):
            if i == id:
        self._bus.write_byte( EXTERNAL_LED_ADDR, 0x00)
        time.sleep(1)
        '''

    def piglow_win(self):
        pyglow = PyGlow(brightness=50, speed=300, pulse=True)
        pyglow.all(0)
        for i in range(1,4):
            pyglow.color('red', speed=200,brightness=100)

        for i in range(1,4):

            pyglow.color('red', speed=400,brightness=50)


            for z in (['orange','yellow','green','blue','white']):
                pyglow.color(z,speed = 100, brightness=(i*60))


        for i in range(3):
            pyglow.all(brightness=255,speed=100)

    def hardware_blip(self):
        self._bus.write_byte( SOUND_ADDR, 0x00)
        self._blip_state = True
        self._blip_timer = BLIP_LENGTH
        #print("Blip")
        
