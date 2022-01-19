from ctre import WPI_TalonSRX
from networktables import NetworkTables

class Shooter:
   def __init__(self, _shooterMotor : WPI_TalonSRX):
      self.shooterMotor = _shooterMotor
   def setSpeed(self,speed):
      self.shooterMotor.set(speed)
   def getCameraInfo(self):
      networkTableData = NetworkTables.getTable("limelight")
      tv = networkTableData.getNumber("tv", None) # valid targets (1 or 0)
      tx = networkTableData.getNumber("tx", None) # horizontal offset (-27 to 27 degrees)
      ty = networkTableData.getNumber("ty", None) # vertical offset (-20.5 to 20.5 degrees)
      ta = networkTableData.getNumber("ta", None) # % of screen covered by target
      data = [tv, tx, ty, (ta * 100)]
      return data
   def hasTarget(self):
      target = self.getCameraInfo()[0]
      if target == 1:
         return True
      else:
         return False



      


      
