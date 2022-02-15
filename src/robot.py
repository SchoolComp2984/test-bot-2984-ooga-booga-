import wpilib, ctre
from utils import ID, pid, math_functions, imutil
from subsystems import rotary_joystick, drive
from networktables import NetworkTables
import math

#py -3 robot.py deploy to deploy the code, all other libraries should be fine.
#Pheonix
class MyRobot(wpilib.TimedRobot):
   COUNTS_PER_RAD = 2048 / (2 * 3.14159)
   RADS_PER_COUNT = 2 * 3.14159 / 2048

   def robotInit(self):

      
      self.pid = pid.PID()
      #Original PID constants: 0.4, 0.001, 3.2
      self.pid.set_pid(0.4, 0.001, 2, 0)

      self.printTimer = wpilib.Timer()
      self.printTimer.start()

      #components: These are classes representing all the electrical sensors and actuators on the robot.
      #self.frontLeft = rev.CANSparkMax(ID.DRIVE_LEFT_FRONT)
      self.frontLeft = ctre.WPI_TalonSRX(ID.DRIVE_LEFT_FRONT)
      self.backLeft = ctre.WPI_TalonSRX(ID.DRIVE_LEFT_BACK)

      self.frontRight = ctre.WPI_TalonSRX(ID.DRIVE_RIGHT_FRONT)
      self.backRight = ctre.WPI_TalonSRX(ID.DRIVE_RIGHT_BACK)

      self.drive_imu = imutil.Imutil(self.backRight)

      # Might change to XBOX controller depending on it working or not.
      self.rotary_controller = rotary_joystick.RotaryJoystick(ID.OPERATOR_CONTROLLER)
      self.operator_controller = wpilib.interfaces.GenericHID(ID.OPERATOR_CONTROLLER)
      self.drive_controller = wpilib.XboxController(ID.DRIVE_CONTROLLER)
      #self.HAND_LEFT = wpilib.interfaces.GenericHID.Hand.kLeftHand
      #self.HAND_RIGHT = wpilib.interfaces.GenericHID.Hand.kRightHand

      #subsystems: These combine multiple components into a coordinated system
      self._drive = drive.Drive(self.frontLeft, self.backLeft, self.frontRight, self.backRight, self.drive_imu, self.pid)

   def teleopInit(self):
      print("Starting")
      self.frontLeft.setInverted(True)
      self.backLeft.setInverted(True)
      self.frontRight.setInverted(False)
      self.backRight.setInverted(False)
      self.rotary_controller.reset_angle(self._drive.getYaw())
      
   def teleopPeriodic(self):
      try:
         if self.operator_controller.getRawButton(0):
            self._drive.arcadeDrive(self.drive_controller.getRawAxis(0),self.drive_controller.getRawAxis(1))
         else:
            angle = self.rotary_controller.rotary_inputs()
            speed = math_functions.interp(self.rotary_controller.getTwist())
            self._drive.absoluteDrive(-speed, angle)
      
         # get trigger axis from controller - brake returns value -1 to 0, gas returns value 0 to 1 
         # leftTrigger = -(self.drive_controller.getTriggerAxis(self.HAND_LEFT)) # brake
         # rightTrigger = self.drive_controller.getTriggerAxis(self.HAND_RIGHT) # gas
         # xAxis = self.drive_controller.getX(self.HAND_LEFT) # left stick x axis for turning
         # self._drive.driftDrive(leftTrigger, rightTrigger, xAxis)


      except:
         raise


if __name__ == "__main__":
   wpilib.run(MyRobot)