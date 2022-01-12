import wpilib, ctre
from utils import ID, pid, math_functions
from subsystems import rotary_joystick, drive
# from frc import smartdashboard

class MyRobot(wpilib.TimedRobot):

   def robotInit(self):
      print("Init")
      
      self.drive_pid = pid.PID()
      self.drive_pid.set_pid(0.4, 0.001, 3.2, 0)
      #components: These are classes representing all the electrical sensors and actuators on the robot.
      self.frontLeft = ctre.WPI_TalonSRX(ID.DRIVE_LEFT_FRONT)
      self.backLeft = ctre.WPI_TalonSRX(ID.DRIVE_LEFT_BACK)

      self.frontRight = ctre.WPI_TalonSRX(ID.DRIVE_RIGHT_FRONT)
      self.backRight = ctre.WPI_TalonSRX(ID.DRIVE_RIGHT_BACK)

      # Left wheels for basic driveable robot were assembled wierdly or something idk lol
      self.frontLeft.setInverted(True)
      self.backLeft.setInverted(True)
      self.frontRight.setInverted(False)
      self.backRight.setInverted(False)

      self.drive_imu = ctre.PigeonIMU(self.backRight)
      self.back_limit_switch = wpilib.DigitalInput(ID.LIMIT_SWITCH_NC)

      # Might change to XBOX controller depending on it working or not.
      self.rJoy = rotary_joystick.RotaryJoystick()
      self.drive_stick = wpilib.Joystick(ID.DRIVE_JOYSTICK)
      self.operator_stick = wpilib.Joystick(ID.OPERATOR_JOYSTICK)
      self.drive_controller = wpilib.XboxController(ID.OPERATOR_JOYSTICK)

      #subsystems: These combine multiple components into a coordinated system.
      self._drive = drive.Drive(self.frontLeft, self.backLeft, self.frontRight, self.backRight, self.drive_imu, self.drive_pid)
      
      #commands: These utilize subsystems to perform autonomous routines.

   def teleopInit(self):
      pass
      
   def teleopPeriodic(self):
      # Exceptions are used to not crash robot code if in competition, 
      # but in our testing case we are raising the exceptions because we want to debug.
      try:
         angle = self.rJoy.rotary_inputs(self)
         speed = math_functions.interp(self.operator_stick.getY())
         print(angle, " ", speed)
         self._drive.absoluteDrive(speed, angle)

         if self.drive_controller.getBackButtonPressed():
            pass
      except:
         raise

      #bussin
         

if __name__ == "__main__":
   wpilib.run(MyRobot)