import wpilib, ctre
from utils import ID, pid, math_functions
from subsystems import rotary_joystick, drive
from networktables import NetworkTables
import math

sd = NetworkTables.getTable('SmartDashboard')

class MyRobot(wpilib.TimedRobot):

   HAND_LEFT = wpilib.interfaces.GenericHID.Hand.kLeftHand
   HAND_RIGHT = wpilib.interfaces.GenericHID.Hand.kRightHand

   def robotInit(self):
      print("starting")

      self.absolute_drive = False

      self.pid = pid.PID()
      self.pid.set_pid(0.4, 0.001, 3.2, 0)
      #components: These are classes representing all the electrical sensors and actuators on the robot.
      self.frontLeft = ctre.WPI_TalonSRX(ID.DRIVE_LEFT_FRONT)
      self.backLeft = ctre.WPI_TalonSRX(ID.DRIVE_LEFT_BACK)

      self.frontRight = ctre.WPI_TalonSRX(ID.DRIVE_RIGHT_FRONT)
      self.backRight = ctre.WPI_TalonSRX(ID.DRIVE_RIGHT_BACK)

      self.drive_imu = ctre.PigeonIMU(self.backRight)

      self.printTimer = wpilib.Timer()
      self.printTimer.start()
      # Might change to XBOX controller depending on it working or not.
      self.rotary_joystick = wpilib.Joystick(1)
      self.rotary_controller = rotary_joystick.RotaryJoystick(self.rotary_joystick)
      self.operator_controller = wpilib.XboxController(ID.OPERATOR_CONTROLLER)
      self.drive_controller = wpilib.XboxController(ID.DRIVE_CONTROLLER)
      #subsystems: These combine multiple components into a coordinated system.
      self._drive = drive.Drive(self.frontLeft, self.backLeft, self.frontRight, self.backRight, self.drive_imu, self.pid)
      
      #commands: These utilize subsystems to perform autonomous routines.

   def teleopInit(self):
      self.frontLeft.setInverted(True)
      self.backLeft.setInverted(True)
      self.frontRight.setInverted(False)
      self.backRight.setInverted(False)
      
   def teleopPeriodic(self):
      #if self.printTimer.hasPeriodPassed(0.5):
         #print(sd.getNumber('robotTime'))
      try:
         right_y = self.drive_controller.getY(self.HAND_RIGHT)
         left_y = self.drive_controller.getY(self.HAND_LEFT)
         self._drive.TankDrive(right_y,left_y)
         

         # if self.drive_controller.getAButtonPressed():
         #    self.absolute_drive = not self.absolute_drive
         #    print(self.absolute_drive)

         # if self.absolute_drive == True:
         #    angle = math.atan2(self.drive_controller.)
         #    # angle = self.rotary_controller.rotary_inputs()
         #    speed = math_functions.interp(self.drive_controller.getY(self.HAND_RIGHT))
         #    self._drive.absoluteDrive(speed, angle)
         # else:
         #    x = self.drive_controller.getX(self.HAND_LEFT)
         #    y = self.drive_controller.getY(self.HAND_LEFT)
         #    self._drive.arcadeDrive(y, x)
      except:
         raise

if __name__ == "__main__":
   wpilib.run(MyRobot)