
import time

###########################################
# servo data classes
###########################################
class ServoStatic:
    def __init__(self, servoDefinition):
        #self.__dict__ = servoDefinition
        self.arduino = servoDefinition['arduino']
        self.pin = servoDefinition['pin']
        self.powerPin = servoDefinition['powerPin']
        self.minComment = servoDefinition['minComment']
        self.maxComment = servoDefinition['maxComment']
        self.minPos = servoDefinition['minPos']
        self.maxPos = servoDefinition['maxPos']
        self.zeroDegPos = servoDefinition['zeroDegPos']
        self.minDeg = servoDefinition['minDeg']
        self.maxDeg = servoDefinition['maxDeg']
        self.autoDetach = servoDefinition['autoDetach']
        self.inverted = servoDefinition['inverted']
        self.restDeg = servoDefinition['restDeg']
        self.enabled = servoDefinition['enabled']
        self.servoType = servoDefinition['servoType']
        self.moveSpeed = servoDefinition['moveSpeed']
        self.cableTerminal = servoDefinition['cableTerminal']
        self.wireColorArduinoTerminal = servoDefinition['wireColorArduinoTerminal']
        self.wireColorTerminalServo = servoDefinition['wireColorTerminalServo']


class ServoType:
    def __init__(self, servoTypeDefinition):
        #self.__dict__ = servoTypeDefinition
        self.typeMinPos = servoTypeDefinition['typeMinPos']
        self.typeMaxPos = servoTypeDefinition['typeMaxPos']
        self.typeInverted = servoTypeDefinition['typeInverted']
        self.typeSpeed = servoTypeDefinition['typeSpeed']
        self.typeTorque = servoTypeDefinition['typeTorque']


class ServoDerived:
    """
    Useful preevaluated values with servo
    """

    def __init__(self, servoStatic, servoType):

        self.servoUniqueId = (servoStatic.arduino * 100) + servoStatic.pin
        self.degRange = servoStatic.maxDeg - servoStatic.minDeg
        self.posRange = servoStatic.maxPos - servoStatic.minPos

        # a servo has normally a shaft rotation speed for a 60° swipe defined
        # this is the maximum speed possible by the servo
        # the inmoov robot has in many cases not a direct shaft connection for a movement
        # but a mechnical gear mechanism
        # for these servos we can define a max move speed of the controlled part
        # msPerPos uses the move speed if it is slower than the servo speed
        # robotControl checks requested move durations against the max speed possible and
        # increases move duration if necessary
        # ATTENTION: servoTypeSpeed is s/60 deg, moveSpeed is ms/60 deg!!
        if (servoStatic.moveSpeed / 1000) > servoType.typeSpeed:
            self.msPerPos = servoStatic.moveSpeed / 60
        else:
            self.msPerPos = servoType.typeSpeed * 1000 / 60


class ServoCurrent:

    def __init__(self, servoName):
        self.servoName = servoName
        self.assigned = False
        self.moving = False
        self.attached = False
        self.autoDetach = 1.0
        self.verbose = False
        self.position = 0
        self.degrees = 0
        self.swiping = False
        self.timeOfLastMoveRequest = time.time()

    def updateData(self, newDegrees, newPosition, newAssigned, newMoving, newAttached, newAutoDetach,
                   newVerbose, newSwiping, newTimeOfLastMoveRequest):
        self.degrees = newDegrees
        self.position = newPosition
        self.assigned = newAssigned
        self.moving = newMoving
        self.attached = newAttached
        self.autoDetach = newAutoDetach
        self.verbose = newVerbose
        self.swiping = newSwiping
        self.timeOfLastMoveRequest = newTimeOfLastMoveRequest

