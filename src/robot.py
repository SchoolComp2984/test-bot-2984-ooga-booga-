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
      self.rotary_joystick = wpilib.Joystick(1)
      self.rotary_controller = rotary_joystick.RotaryJoystick(self.rotary_joystick)
      self.rotary_buttons = wpilib.interfaces.GenericHID(ID.OPERATOR_CONTROLLER)
      self.operator_controller = wpilib.XboxController(ID.OPERATOR_CONTROLLER)
      self.drive_controller = wpilib.XboxController(ID.DRIVE_CONTROLLER)
      self.HAND_LEFT = wpilib.interfaces.GenericHID.Hand.kLeftHand
      self.HAND_RIGHT = wpilib.interfaces.GenericHID.Hand.kRightHand

      #subsystems: These combine multiple components into a coordinated system.
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

         # if self.rotary_buttons.getRawButton(1):
         #    # also check if shooter has balls before aiming so we can stop the shooter from running when we finish shooting.
         #    self._shoot.execute()
         #    self.rotary_controller.reset_angle(self._shoot.target_angle)
         # else:
         #    angle = self.rotary_controller.rotary_inputs()
         #    speed = math_functions.interp(self.rotary_controller.getTwist())
         #    self._drive.absoluteDrive(-speed, angle)
         
         #Experimental Stuff by Kyle 2
         self.servoangle = (self.drive_controller.getRightX() + 1) * 90
         self.firstservo.setAngle(self.servoangle)
         if self.rotary_buttons.getRawButton(2):
            self.firstservo.setAngle(0)
         if self.rotary_buttons.getRawButton(3):
            self.firstservo.setAngle(180)

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