import wpilib, ctre
from utils import ID, PID, math_functions
from subsystems import rotary_joystick, drive
# from frc import smartdashboard

class MyRobot(wpilib.TimedRobot):

   HAND_LEFT = wpilib.interfaces.GeneericHID.Hand.kLeftHand
   HAND_RIGHT = wpilib.interfaces.GenericHID.Hand.kRightHand

   def robotInit(self):
      print("starting")

      self.absolute_drive = False

      self.pid = PID.PID()
      self.pid.set_pid(0.4, 0.001, 3.2, 0)
      #components: These are classes representing all the electrical sensors and actuators on the robot.
      self.frontLeft = ctre.WPI_TalonSRX(ID.DRIVE_LEFT_FRONT)
      self.backLeft = ctre.WPI_TalonSRX(ID.DRIVE_LEFT_BACK)

      self.frontRight = ctre.WPI_TalonSRX(ID.DRIVE_RIGHT_FRONT)
      self.backRight = ctre.WPI_TalonSRX(ID.DRIVE_RIGHT_BACK)

      self.drive_imu = ctre.PigeonIMU(self.backRight)
      self.back_limit_switch = wpilib.DigitalInput(ID.LIMIT_SWITCH_NC)

      # Might change to XBOX controller depending on it working or not.
      self.rotary_joystick = wpilib.Joystick(0)
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
      # Exceptions are used to not crash robot code if in competition, 
      # but in our testing case we are raising the exceptions because we want to debug.
      try:
         angle = self.rotary_controller.rotary_inputs()
         speed = math_functions.interp(self.operator_stick.getY())
         x = self.drive_controller.getX(self.HAND_LEFT)
         y = self.drive_controller.getY(self.HAND_LEFT)

         print(angle, " ", speed)
         if self.drive_controller.getAButtonPressed():
            self.absolute_drive = not self.absolute_drive

         if self.absolute_drive == True:
            self._drive.absoluteDrive(speed, angle)
         else:
            self._drive.arcadeDrive(y, x)
      except:
         raise

      #print("hi")
         

if __name__ == "__main__":
   wpilib.run(MyRobot)