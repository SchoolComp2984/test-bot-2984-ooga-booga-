from subsystems import drive, shooter

class Shoot:
   TURNING = 0
   SHOOTING = 1
   state = -1

   def __init__(self, _drive, _shooter):
      self.drive = _drive
      self.shooter = _shooter

   def main(self):
      if self.shooter.hasTarget:
         if self.state == self.TURNING:
            pass
         elif self.state == self.SHOOTER:
            pass
