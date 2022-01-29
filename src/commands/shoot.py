from subsystems.drive import Drive
from subsystems.shooter import Shooter

class Shoot:
   TURNING = 0
   SHOOTING = 1
   DEFAULT = -1
   state = TURNING

   def __init__(self, _drive : Drive, _shooter : Shooter):
      self.drive = _drive
      self.shooter = _shooter
      self.target_angle = self.drive.getYaw() - 180

   def move(self):
       self.drive.absoluteDrive(0, self.target_angle)

   def turning(self):
      if self.shooter.hasTarget(): # check if robot has target
         delta_angle = self.shooter.getCameraInfo()[1] # get angle of target
         self.target_angle = self.drive.getYaw() - delta_angle
         if abs(delta_angle) < 2: # if aim is accurate enough
            self.state = self.SHOOTING # set state to shooting
            print ("State is shooting")
      self.move()

   def shoot(self):
      pass
   
   def execute(self):
      if self.state == self.TURNING:
         self.turning()
      
      if self.state == self.SHOOTING: # if or elif
         #Code for shoot the ball
         self.shoot()
         #if shooting is done:
         self.finish()

   def finish(self):
      self.state = self.TURNING