import wpilib, ctre, rev
from commands import shoot
from utils import ID, pid, math_functions, imutil
from subsystems import rotary_joystick, drive, shooter
from networktables import NetworkTables
import math

sd = NetworkTables.getTable('SmartDashboard')

class MyRobot(wpilib.TimedRobot):

   def robotInit(self):

      self.pid = pid.PID()
      #Original PID constants: 0.4, 0.001, 3.2
      self.pid.set_pid(0.4, 0.001, 2, 0)

      self.printTimer = wpilib.Timer()
      self.printTimer.start()

      # self.NOBALL = 0
      # self.BLUE = 1
      # self.RED = 2
      # self.alliance_color = self.RED
      # self.ball_color = self.NOBALL
      # self.driver_station = wpilib.DriverStation
      # self.alliance = self.driver_station.getAlliance()
      # # To access what type of alliance it is: wpilib.DriverStation.Alliance.kBlue
      # if wpilib.DriverStation.Alliance.kBlue == self.alliance:
      #    self.alliance_color = self.BLUE
      # else:
      #    self.alliance_color = self.RED

      #components: These are classes representing all the electrical sensors and actuators on the robot.
      #self.frontLeft = rev.CANSparkMax(ID.DRIVE_LEFT_FRONT)
      self.frontLeft = ctre.WPI_TalonSRX(ID.DRIVE_LEFT_FRONT)
      self.backLeft = ctre.WPI_TalonSRX(ID.DRIVE_LEFT_BACK)

      self.frontRight = ctre.WPI_TalonSRX(ID.DRIVE_RIGHT_FRONT)
      self.backRight = ctre.WPI_TalonSRX(ID.DRIVE_RIGHT_BACK)

      self.shooterMotor = ctre.WPI_TalonFX(ID.SHOOTER)

      self.drive_imu = imutil.Imutil(self.backRight)

      # self.color_sensor = rev.ColorSensorV3(wpilib.I2C.Port(0))
      self.testServo = wpilib.Servo(0)

      # Might change to XBOX controller depending on it working or not.
      self.rotary_controller = rotary_joystick.RotaryJoystick(ID.OPERATOR_CONTROLLER)
      self.operator_controller = wpilib.interfaces.GenericHID(ID.OPERATOR_CONTROLLER)
      self.drive_controller = wpilib.XboxController(ID.DRIVE_CONTROLLER)

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

         self.testServo.setAngle(self.drive_controller.getLeftX() * 180 - 90)
         
         # if self.color_sensor.getIR():
         #    if self.color_sensor.getColor()[0] < self.color_sensor.getColor()[2]:
         #       self.ball_color = self.BLUE
         #    else:
         #       self.ball_color = self.RED
         #    if self.ball_color == self.alliance_color:
         #       print("shoot")
         #    else: 
         #       print("discard")
         # else:
         #    self.ball_color = self.NOBALL

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
         # leftTrigger = -(self.drive_controller.getTriggerAxis(self.HAND_LEFT)) # brake
         # rightTrigger = self.drive_controller.getTriggerAxis(self.HAND_RIGHT) # gas
         # xAxis = self.drive_controller.getX(self.HAND_LEFT) # left stick x axis for turning
         # self._drive.driftDrive(leftTrigger, rightTrigger, xAxis)


      except:
         raise


if __name__ == "__main__":
   wpilib.run(MyRobot)