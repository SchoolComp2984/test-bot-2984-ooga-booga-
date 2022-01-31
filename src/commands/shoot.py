from subsystems.drive import Drive
from subsystems.shooter import Shooter

class Shoot:
   TURNING = 0
   MOVING = 1
   SHOOTING = 2
   DEFAULT = -1
   state = TURNING

   def __init__(self, _drive : Drive, _shooter : Shooter):
      self.drive = _drive
      self.shooter = _shooter
      self.target_angle = self.drive.getYaw() - 180

   def turning(self):
    if self.shooter.hasTarget(): # check if robot has target
        delta_angle = self.shooter.getCameraInfo()[1] # get angle of target
        self.target_angle = self.drive.getYaw() - delta_angle
        if abs(delta_angle) < 2: # if aim is accurate enough
            self.state = self.MOVING # set state to shooting
    self.drive.absoluteDrive(0, self.target_angle)

    def moving(self):
        pass

    def shooting(self):
        pass
   
   def execute(self):
      if self.state == self.TURNING:
         self.turning()
      if self.state == self.MOVING:
          self.moving()
      if self.state == self.SHOOTING: # if or elif
         #Code for shoot the ball
         self.shooting()
         #if shooting is done:
         self.finish()

   def finish(self):
      self.state = self.TURNING