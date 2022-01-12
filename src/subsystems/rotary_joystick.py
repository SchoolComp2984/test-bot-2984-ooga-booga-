class RotaryJoystick():
    def rotary_inputs(self, robot):
        x=robot.drive_stick.getX()
        y=robot.drive_stick.getY()
        z=robot.drive_stick.getZ()
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
        return angle