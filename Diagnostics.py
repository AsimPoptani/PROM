import math
from IO import readInputs

max_bar_length = 10
## Input variables
switch_A_1 = False
switch_A_2 = False
knob_A = 0
switch_B_1 = False
switch_B_2 = False
knob_B = 0

def cursorTo(x, y):
    #move the cursor on the screen to location x,y
    return '\u001b[' +  str(y) + ';'  + str(x) + 'H'
input_handler = readInputs.InputHandler()



## Setup phase
print(cursorTo(34, 0))
print("\u001b[2J")

print("\u001b[0m--Diagnostics--\n")
print(cursorTo(0, 3))
print("\u001b[0mController 1")
print(cursorTo(0, 4))
print("\u001b[0mButton 1 [ ]  Button2 [ ]")
print(cursorTo(0, 5))
print("\u001b[0mKnob <          >")

print(cursorTo(0, 7))
print("\u001b[0mController 2")
print(cursorTo(0, 8))
print("\u001b[0mButton 1 [ ]  Button2 [ ] ")
print(cursorTo(0, 9))
print("\u001b[0mKnob <          >")

#hide cursor
print("\u001b[?25l")

def updateDiagnostic():
    global switch_A_1, switch_A_2, knob_A, knob_B, switch_B_1, switch_B_2
    input_handler.update()

    ## Update screen
    if input_handler.get_switch_A1() and not switch_A_1:
        print(cursorTo(11, 5) + "x")
        switch_A_1 = input_handler.get_switch_A1()
    elif not input_handler.get_switch_A1() and switch_A_1:
        print(cursorTo(11, 5) + " ")
        switch_A_1 = input_handler.get_switch_A1()

    if input_handler.get_switch_A2() and not switch_A_2:
        print(cursorTo(24, 5) + "x")
        switch_A_2 = input_handler.get_switch_A2()
    elif not input_handler.get_switch_A2() and switch_A_2:
        print(cursorTo(24, 5) + " ")
        switch_A_2 = input_handler.get_switch_A2()

    if not round(input_handler.get_knob_A(), 1) == round(knob_A, 1):
        knob_A = input_handler.get_knob_A()
        bars = math.floor((max_bar_length+1)*knob_A)
        print(cursorTo(7, 6)+"\u001b[0m"+("+"*bars)+(" "*(max_bar_length-bars)) +"> " + "Scaled: [" + str(round(input_handler.get_knob_A(),2)) + "] Raw: [" + str(int(input_handler._knob_A_raw)) + "]  ")

    if input_handler.get_switch_B1() and not switch_B_1:
        print(cursorTo(11, 9) + "x")
        switch_B_1 = input_handler.get_switch_B1()
    elif not input_handler.get_switch_B1() and switch_B_1:
        print(cursorTo(11, 9) + " ")
        switch_B_1 = input_handler.get_switch_B1()

    if input_handler.get_switch_B2() and not switch_B_2:
        print(cursorTo(24, 9) + "x")
        switch_B_2 = input_handler.get_switch_B2()
    elif not input_handler.get_switch_B2() and switch_B_2:
        print(cursorTo(24, 9) + " ")
        switch_B_2 = input_handler.get_switch_B2()

    if not round(input_handler.get_knob_B(), 1) == round(knob_B, 1):
        knob_B = input_handler.get_knob_B()
        bars = math.floor((max_bar_length+1)*knob_B)
        print(cursorTo(7, 10)+("+"*bars)+(" "*(max_bar_length-bars)) +"> " + "Scaled: [" + str(round(input_handler.get_knob_B(),2)) + "] Raw: [" + str(int((sum(input_handler._dac_average_table) / 3) - readInputs.KNOB_B_MIN)) + "]  ")
