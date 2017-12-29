import sys
import time 
from Phidget22.Devices.Stepper import *
from Phidget22.PhidgetException import *
from Phidget22.Phidget import *
from Phidget22.Net import *
import math
import time
class Motor:

  def __init__(self, id):
    # Instantiate the servos
    self.id = id
    self.accl = 800
    self.velocity = 2000
    self.target = 0
    self.progress = 0
    self.position = 0 
    self.start_position = self.position
    self.initialized = False
    self.ch = self.attach_stepper(id)
    self.initialized = True
    print "%d: Motor initialized. Start=%d Position=%d Target=%d" %(self.id, self.start_position, self.position, self.target)
 
  def attach_stepper(self, id):
    try:
      ch = Stepper() 
      ch.setOnAttachHandler(self.StepperAttached)
      ch.setOnDetachHandler(self.StepperDetached)
      ch.setOnErrorHandler(self.ErrorEvent)
      ch.setOnPositionChangeHandler(self.PositionChangeHandler)
      ch.setDeviceSerialNumber(id) 

      print(id,": Waiting for the Phidget Stepper Object to be attached...")
      ch.openWaitForAttachment(5000)
    except PhidgetException as e:
      print(id, ": Phidget Exception %i: %s" % (e.code, e.details))
      exit(1)

    print("Engaging the motor %d" % id)
    ch.setEngaged(1)
    print("Created motor %d" %id)
    print("Acceleration Range [%d,%d] : %d" % (ch.getMinAcceleration(), ch.getMaxAcceleration(), ch.getAcceleration()))
    print("Velocity Range [%d,%d] : %d" % (ch.getMinVelocityLimit(), ch.getMaxVelocityLimit(), ch.getVelocityLimit()))
    #print("Position Range [%d,%d] : %d" % (ch.getMinPosition(), ch.getMaxPosition(), ch.getPosition()))
    print("CurrentLimit Range [%d,%d] : %d" % (ch.getMinCurrentLimit(), ch.getMaxCurrentLimit(), ch.getCurrentLimit()))
    ch.setCurrentLimit(3)
    return ch

  def StepperAttached(self, e):
    try:
        attached = e
        print("Attach Event Detected (Information Below)")
        print("===========================================")
        print("Library Version: %s" % attached.getLibraryVersion())
        print("Serial Number: %d" % attached.getDeviceSerialNumber())
        print("Channel: %d" % attached.getChannel())
        print("Channel Class: %s" % attached.getChannelClass())
        print("Channel Name: %s" % attached.getChannelName())
        print("Device ID: %d" % attached.getDeviceID())
        print("Device Version: %d" % attached.getDeviceVersion())
        print("Device Name: %s" % attached.getDeviceName())
        print("Device Class: %d" % attached.getDeviceClass())
        print("\n")

    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))
        print("Press Enter to Exit...\n")
        readin = sys.stdin.read(1)
        exit(1)   
    
  def StepperDetached(self, e):
    detached = e
    try:
        print("Detach event on Port %d Channel %d" % (detached.getHubPort(), detached.getChannel()))
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))
        print("Press Enter to Exit...\n")
        readin = sys.stdin.read(1)
        exit(1)   

  def ErrorEvent(self, e, eCode, description):
    print("Error %i : %s" % (eCode, description))

  def turn(self, steps):
    self.start_position = self.position
    self.target = self.start_position + steps    
    self.ch.setAcceleration(self.accl)
    self.ch.setVelocityLimit(self.velocity)
    self.ch.setTargetPosition(self.target)
    print "%d: Motor.turn: Steps=%d Target=%d Position=%d Start=%d" % (self.id, steps, self.target, self.position, self.start_position)
  
  def stop(self):
    self.ch.setVelocityLimit(0)

  def PositionChangeHandler(self, e, position):
    if not self.initialized:
      # Ignore any spurious callbacks during initialization
      return
    if self.target != self.start_position:
      self.progress = (position - self.start_position)*100/(self.target-self.start_position)
    self.position = position
    #print("%d: Position: Dev=%d T=%d P=%d Pro=%f %%" % (self.id, e.getDeviceSerialNumber(), self.target, position, self.progress))

  def isDone(self):
    return math.fabs(self.position - self.target) < 1

  def wait(self):
    print "%d: Motor.wait: position=%d target=%d" %(self.id, self.position, self.target)
    while not self.isDone():
      time.sleep(1)
      print self.id, ": Motor wait Position=", self.position, " Target=", self.target, " Progress=", self.progress
