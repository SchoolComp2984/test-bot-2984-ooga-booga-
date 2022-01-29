from dbm import _ValueType
from re import X
from ctre import WPI_TalonSRX, PigeonIMU
import math
from utils import pid, imutil

# parameter : type
class Drive:
   #CONTRUCTOR
   def __init__(self, _frontLeft : WPI_TalonSRX, _backLeft : WPI_TalonSRX, _frontRight : WPI_TalonSRX, _backRight : WPI_TalonSRX, _drive_imu : imutil, _pid : pid):
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
      cur_rotation = self.drive_imu.getYaw()
        # finds angle difference (delta angle) in range -180 to 180
      delta_angle = desired_angle - cur_rotation
      delta_angle = ((delta_angle + 180) % 360) - 180
        # PID steering power limited between -12 and 12
      steer = max(-12, min(12, self.pid.steer_pid(delta_angle)))
      left_speed = speed / 12
      right_speed = speed / 12
      left_speed -= steer / 12
      right_speed += steer / 12
        #self._drive.DifferentialDrive(left, right)
      # self._drive.arcadeDrive(left,steer)
      # Use PID or something in this next step idk
      self.setSpeed(left_speed, right_speed)

   #Drive method for mecanum wheels
   def mecanumDrive(self, joy_y, joy_x, desired_angle):
      #Set power without turning
      self.flspeed = joy_y + joy_x
      self.frspeed = joy_y - joy_x
      self.brspeed = self.flspeed
      self.blspeed = self.frspeed
      #Add turning
      cur_rotation = self.drive_imu.getYaw()
      delta_angle = desired_angle - cur_rotation
      delta_angle = ((delta_angle + 180) % 360) - 180
      steer = max(-1, min(1, self.pid.steer_pid(delta_angle)/12))
      self.flspeed -= steer
      self.frspeed += steer
      self.blspeed -= steer
      self.brspeed += steer
      #Set speed for all wheels
      self.frontLeft.set(self.flspeed)
      self.frontRight.set(self.frspeed)
      self.backLeft.set(self.blspeed)
      self.backRight.set(self.brspeed)

   def getCombined(self, combined, x):
      leftSpeed = combined
      rightSpeed = combined

      if x > 0:
         rightSpeed += x
      elif x < 0:
         leftSpeed += x

      return [leftSpeed, rightSpeed]

   def setDriftSpeeds(self, combined, x):
      speeds = self.getCombined(combined, x)
      self.setSpeed(2 * speeds[0], 2 * speeds[1])

   def stop(self):
      self.setSpeed(0, 0)
   