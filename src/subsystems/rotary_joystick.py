import wpilib

class RotaryJoystick():
    def __init__(self, _rotary_joystick : wpilib.Joystick):
        self.rotary_joystick = _rotary_joystick
        self.angleoffset = 0.0

    def rotary_inputs(self):
        x= self.rotary_joystick.getX()
        y= self.rotary_joystick.getY()
        z= self.rotary_joystick.getZ()
        MAX=max(x, y, z)
        MIN=min(x, y, z)
        if((x<=y) and (y<=z)):
            mid=y  
            angle=60-(mid-MIN)/(MAX-MIN)*60
        if((y<=x) and (x<=z)):
            mid=x
            angle=60+(mid-MIN)/(MAX-MIN)*60
        if((y<=z) and (z<=x)):
            mid=z
            angle=180-(mid-MIN)/(MAX-MIN)*60
        if((z<=y) and (y<=x)):
            mid=y
            angle=180+(mid-MIN)/(MAX-MIN)*60
        if((z<=x) and (x<=y)):
            mid=x
            angle=300-(mid-MIN)/(MAX-MIN)*60
        if((x<=z) and (z<=y)):
            mid=z
            angle=300+(mid-MIN)/(MAX-MIN)*60
        #print ("a=", angle)
        angle = angle + self.angleoffset
        return angle
    
    def reset_angle(self,angle):
        self.angleoffset = 0.0
        self.angleoffset = angle - self.rotary_inputs()

