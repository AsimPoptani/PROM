import smbus
import time
from serial import Serial

##Read inputs from I2C controllers and provide in friendly form

INPUT_ADDR = 0x3d
ADC_ADDR = 0x21
ADC_COMMAND = 0b00010000
DAC_ADDR = 0x3c
KNOB_A_MAX = 3312
KNOB_A_MIN = 435
KNOB_B_MAX = 31
KNOB_B_MIN = 0

timer_cycles = 3

class SensorHandler():

    def __init__(self):
        self._bus = smbus.SMBus(1)
        self._raw_input = 0xfa
        self._knob_A_raw = 0

        ## Buttons
        self._switch_A_1 = False
        self._switch_A_2 = False
        self._switch_B_1 = False
        self._switch_B_2 = False

        self._switch_A_1_timer = 0
        self._switch_A_2_timer = 0
        self._switch_B_1_timer = 0

        ## Knobs
        self._knob_A = 0
        self._knob_B = 0
        self._dac_estimator = 0
        self._dac_average_table = [0, 0, 0]

    def update(self):
        self._raw_input = self._bus.read_byte( INPUT_ADDR )
        #print(bin(self._raw_input))
        self._update_dac()

        ## Decrement debounce timers
        if self._switch_A_1_timer != 0:
            self._switch_A_1_timer -= 1
        if self._switch_A_2_timer != 0:
            self._switch_A_2_timer -= 1
        if self._switch_B_1_timer != 0:
            self._switch_B_1_timer -= 1

        ## Software debounced
        if str(bin(self._raw_input))[9] == '0':
            if self._switch_A_1_timer == 0:
                self._switch_A_1 = True
                self._switch_A_1_timer = timer_cycles
        else:
            if self._switch_A_1_timer == 0:
                self._switch_A_1 = False
                self._switch_A_1_timer = timer_cycles

        if str(bin(self._raw_input))[8] == '0':
            if self._switch_A_2_timer == 0:
                self._switch_A_2 = True
                self._switch_A_2_timer = timer_cycles
        else:
            if self._switch_A_2_timer == 0:
                self._switch_A_2 = False
                self._switch_A_2_timer = timer_cycles

        if str(bin(self._raw_input))[7] == '0':
            if self._switch_B_1_timer == 0:
                self._switch_B_1 = True
                self._switch_B_1_timer = timer_cycles
        else:
            if self._switch_B_1_timer == 0:
                self._switch_B_1 = False
                self._switch_B_1_timer = timer_cycles

        ## This logic is flipped because of the hardware debouncer's NOT gate
        if str(bin(self._raw_input))[6] == '0':
            self._switch_B_2 = False
        else:
            self._switch_B_2 = True

        ## Knobs
        self._bus.write_byte( ADC_ADDR, ADC_COMMAND )
        read_string = str(bin(self._bus.read_word_data( ADC_ADDR, 0x00 )))[2:]
        read_string = "0"*(16-len(read_string))+read_string

        A = read_string[:4]
        B = read_string[4:8]
        D = read_string[-4:]
        read_string = int(D + A + B, 2)
        self._knob_A_raw = read_string
        self._knob_A = (read_string - KNOB_A_MIN) / (KNOB_A_MAX - KNOB_A_MIN)

    def _dac_rearranger(self,in_num):
        ## Takes value between 0 and 31, returns integer to set on output to recieve that value on DAC
        mapping_table = [5,6,7,1,3,4,0,2]
        output_table = ["0" for i in range(8)]

        if not 0 <= int(in_num) <= 31:
            Exception("DAC can only represent between 0 and 31")
        in_table = ["0" for i in range(10-len(str(bin(in_num))))] + list(str(bin(in_num))[2:])

        for i in range(8):
            output_table[mapping_table[i]] = in_table[i]

        out_num = int("".join(output_table), 2)

        return out_num

    def _dac_write(self, value):
        self._bus.write_byte( DAC_ADDR , value )

    def _dac_overshoot(self):
        ## Returns true if the DAC estimator is greater than the voltage recieved from the variable resistor
        bytes_in = self._bus.read_byte( DAC_ADDR)
        bytes_table = ["0" for i in range(10-len(str(bin(bytes_in))))] + list(str(bin(bytes_in)[2:]))
        if bytes_table[5] == "1":
            #print("estimator overshot")
            return True
        else:
            #print("estimator undershot")
            return False

    def _update_dac(self):
        ## Sets the value of _knob_B to the valus true if the DAC ese recieved from the DAC - ADC
        self._dac_write(self._dac_rearranger(self._dac_estimator))
        #print(self._dac_estimator)
        if self._dac_overshoot():
            if not self._dac_estimator <= KNOB_B_MIN:
                self._dac_estimator -= 1
        else:
            if not self._dac_estimator >= KNOB_B_MAX:
                self._dac_estimator += 1



        ## Calculate a moving average of the last 3 results for stability
        self._dac_average_table[2] = self._dac_average_table[1]
        self._dac_average_table[1] = self._dac_average_table[0]
        self._dac_average_table[0] = self._dac_estimator

        self._knob_B = ((sum(self._dac_average_table) / 3) - KNOB_B_MIN) / (KNOB_B_MAX - KNOB_B_MIN)


    def get_switch_A1(self):
        return self._switch_A_1

    def get_switch_A2(self):
        return self._switch_A_2

    def get_switch_B1(self):
        return self._switch_B_1

    def get_switch_B2(self):
        #print("switch", self._switch_B_2)
        return self._switch_B_2

    def get_knob_A(self):
        if 0 <= self._knob_A <= 1:
            return self._knob_A
        elif self._knob_A < 0:
            return 0
        else:
            return 1

    def get_knob_B(self):
        if 0 <= self._knob_B <= 1:
            return self._knob_B
        elif self._knob_B < 0:
            return 0
        else:
            return 1
