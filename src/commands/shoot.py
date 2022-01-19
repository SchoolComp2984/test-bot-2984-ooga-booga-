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

   def execute(self):
      if self.state == self.TURNING:
         #Put a copy of this if in robot.py to have a starting angle for the first shoot
         if self.shooter.hasTarget():
            delta_angle = self.shooter.getCameraInfo()[1]
            self.target_angle = self.drive.getYaw() - delta_angle
            if abs(delta_angle) < 2:
               self.state = self.SHOOTING
               print ("State is shooting")
         self.drive.absoluteDrive(0, self.target_angle)
      elif self.state == self.SHOOTING:
         #Code for shoot the ball
         #if shooting is done:
         self.finish()
   def finish(self):
      self.state = self.TURNING
