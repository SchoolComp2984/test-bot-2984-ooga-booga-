from ctre import WPI_TalonSRX, PigeonIMU
import math
from utils import pid

# parameter : type
class Drive:
   #CONTRUCTOR
   def __init__(self, _frontLeft : WPI_TalonSRX, _backLeft : WPI_TalonSRX, _frontRight : WPI_TalonSRX, _backRight : WPI_TalonSRX, _drive_imu : PigeonIMU, _pid : pid):
      self.frontLeft = _frontLeft
      self.backLeft = _backLeft

      self.frontRight = _frontRight
      self.backRight = _backRight
      
      self.drive_imu = _drive_imu
      self.pid = _pid
   #HELPER FUNCTIONS
   def setRightSpeed(self, speed):
      # speed is a float value from -1 to 1
      speed = max(-1, min(speed, 1))
      self.frontRight.set(speed)
      self.backRight.set(speed)

   def setLeftSpeed(self, speed):
      # speed is a float value from -1 to 1
      speed = max(-1, min(speed, 1))
      self.frontLeft.set(speed)
      self.backLeft.set(speed)
   
   def setSpeed(self, left, right):
      self.setLeftSpeed(left)
      self.setRightSpeed(right)

   def getRotation(self):
        # Get the yaw from the IMU
        return self.drive_imu.getYawPitchRoll()[1]

   def getYaw(self):
        return self.getRotation()[0]

   #DRIVE FUNCTIONS
   def arcadeDrive(self, y, x):
      left_speed = y + x
      right_speed = y - x
      self.setSpeed(left_speed, right_speed)

   def TankDrive(self, right_y, left_y):
      left_speed = left_y / 2
      right_speed = right_y / 2
      self.setSpeed(left_speed, right_speed)

      

   def absoluteDrive(self, speed, desired_angle):
      # speed is a float value from -1 to 1
      cur_rotation = self.getYaw()
        # finds angle difference (delta angle) in range -180 to 180
      delta_angle = desired_angle - cur_rotation # self.drive_imu.getAbsoluteCompassHeading()
      delta_angle = ((delta_angle + 180) % 360) - 180
        # PID steering power limited between -12 and 12
      steer = max(-12, min(12, self.pid.steer_pid(delta_angle)))
      left_speed = speed / 120
      right_speed = speed / 120
      left_speed -= steer / 12
      right_speed += steer / 12
        #self._drive.DifferentialDrive(left, right)
      # self._drive.arcadeDrive(left,steer)
      # Use PID or something in this next step idk
      self.setSpeed(left_speed, right_speed)
      # this function is NOT finished. It should be based on a two axis joystick determing rotation and one 
      # joystick controlling the speed. The motors should rotate to the angle a two axis joystick points