from IO import xbox
class TestSensorHandler():
    def __init__(self):
        self.joystick=xbox.Joystick()
    def update(self):
        pass

    def get_switch_A1(self):
        return self.joystick.Y()
    
    def get_switch_A2(self):
        return self.joystick.B()

    def get_switch_B1(self):
        return self.joystick.X()

    
    def get_switch_B2(self):
        return self.joystick.A()
    
    def get_knob_A(self):
        return abs(self.joystick.leftX())

    def get_knob_B(self):
        return abs(self.joystick.rightX())