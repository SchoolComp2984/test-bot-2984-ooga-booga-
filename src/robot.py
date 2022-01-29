from turtle import right
import wpilib, ctre
from commands import shoot
from utils import ID, pid, math_functions, imutil
from subsystems import rotary_joystick, drive, shooter
from networktables import NetworkTables
import math
import rev

sd = NetworkTables.getTable('SmartDashboard')

class MyRobot(wpilib.TimedRobot):

   def robotInit(self):
      print("starting")

      #Experimental Stuff by Kyle
      self.servoangle = 90
      self.firstservo = wpilib.Servo(0)

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

      self.shooterMotor = ctre.WPI_TalonFX(ID.SHOOTER)

      self.drive_imu = imutil.Imutil(self.backRight)

      # Might change to XBOX controller depending on it working or not.
      self.HAND_LEFT = wpilib.interfaces.GenericHID.Hand.kLeftHand
      self.HAND_RIGHT = wpilib.interfaces.GenericHID.Hand.kRightHand
      self.rotary_controller = rotary_joystick.RotaryJoystick(ID.OPERATOR_CONTROLLER)
      self.operator_controller = wpilib.interfaces.GenericHID(ID.OPERATOR_CONTROLLER)
      self.drive_controller = wpilib.XboxController(ID.DRIVE_CONTROLLER)

      # xbox controller for drifting system
      self.controller = wpilib.XboxController(1)

      #subsystems: These combine multiple components into a coordinated system
      self._drive = drive.Drive(self.frontLeft, self.backLeft, self.frontRight, self.backRight, self.drive_imu, self.pid)
      self._shooter = shooter.Shooter(self.shooterMotor)

      #commands: These utilize subsystems to perform autonomous routines.
      self._shoot = shoot.Shoot(self._drive, self._shooter)

   def teleopInit(self):
      self.frontLeft.setInverted(True)
      self.backLeft.setInverted(True)
      self.frontRight.setInverted(False)
      self.backRight.setInverted(False)
      self.rotary_controller.reset_angle(self._drive.getYaw())
      
   def teleopPeriodic(self):
      try:
         
         # if self.printTimer.hasPeriodPassed(0.5):
         #    print(self._shooter.getCameraInfo())

         # if self.operator_controller.getRawButton(1):
         #    # also check if shooter has balls before aiming so we can stop the shooter from running when we finish shooting.
         #    self._shoot.execute()
         #    self.rotary_controller.reset_angle(self._shoot.target_angle)
         # else:
         #    angle = self.rotary_controller.rotary_inputs()
         #    speed = math_functions.interp(self.rotary_controller.getTwist())
         #    self._drive.absoluteDrive(-speed, angle)
         
         # get trigger axis from controller - brake returns value -1 to 0, gas returns value 0 to 1 
         leftTrigger = -(self.controller.getLeftTriggerAxis()) # brake
         rightTrigger = self.controller.getRightTriggerAxis() # gas
         xAxis = self.controller.getLeftX() # left stick x axis for turning

         if leftTrigger < 0 and rightTrigger > 0: # if brake and gas is pressed
            combinedTriggers = leftTrigger + rightTrigger
            self.drive.setDriftSpeeds(combinedTriggers, xAxis)
            
         elif leftTrigger < 0: # if brake is pressed
            self.drive.setDriftSpeeds(leftTrigger, xAxis)

         elif rightTrigger > 0: # if gas is pressed
            self.drive.setDriftSpeeds(rightTrigger, xAxis)

         else: # if neither one is pressed
            self.drive.stop()

         # print(self.drive_controller.getLeftY)
         # print(self.drive_controller.getLeftX)
         # print(self.drive_controller.getLeftY + self.drive_controller.getLeftX)
         #right_y = self.drive_controller.getY(self.HAND_RIGHT)
         #left_y = self.drive_controller.getY(self.HAND_LEFT)
         #self._drive.TankDrive(right_y,left_y)
         #x = self.drive_controller.getX(self.HAND_LEFT)
         #y = self.drive_controller.getY(self.HAND_LEFT)
         #self._drive.arcadeDrive(y, x)
         #self._drive.mecanumDrive()
      except:
         raise


if __name__ == "__main__":
   wpilib.run(MyRobot)