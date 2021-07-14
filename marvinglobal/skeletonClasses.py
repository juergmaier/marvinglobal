
import time
from dataclasses import dataclass, field

###########################################
# servo data classes
###########################################
@dataclass
class ServoType:

    def updateValues(self, servoTypeDefinition):
        self.typeMinPos = servoTypeDefinition['typeMinPos']
        self.typeMaxPos = servoTypeDefinition['typeMaxPos']
        self.typeInverted = servoTypeDefinition['typeInverted']
        self.typeSpeed = servoTypeDefinition['typeSpeed']
        self.typeTorque = servoTypeDefinition['typeTorque']


@dataclass
class ServoStatic:
    def updateValues(self, servoDefinition):
        self.arduinoIndex = servoDefinition['arduinoIndex']
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

    def degFromPos(self, inPos: int):
        # inPos has to be in the 0..180 range (servo.write() limits this)
        # minPos has to be smaller than maxPos. Inversion is handled in the arduino
        # minDegrees always has to be smaller than maxDegrees
        degPerPos = abs(self.maxDeg-self.minDeg) / abs(self.maxPos-self.minPos)
        deltaPos = inPos - self.zeroDegPos

        degrees = deltaPos * degPerPos
        # print(f"degrees: {degrees}")
        return round(degrees)


@dataclass
class ServoFeedback:
    i2cMultiplexerAddress = 0
    i2cMultiplexerChannel = 0
    kp = 0.0
    ki = 0.0
    kd = 0.0
    degreesFactor = 1.0
    feedbackInverted = 0

    def updateValues(self, servoFeedbackDefinition):
        self.i2cMultiplexerAddress = servoFeedbackDefinition['i2cMultiplexerAddress']
        self.i2cMultiplexerChannel = servoFeedbackDefinition['i2cMultiplexerChannel']
        self.kp = servoFeedbackDefinition['kp']
        self.ki = servoFeedbackDefinition['ki']
        self.kd = servoFeedbackDefinition['kd']
        self.degPerPos = servoFeedbackDefinition['degPerPos']
        self.feedbackInverted = servoFeedbackDefinition['feedbackInverted']


@dataclass
class ServoDerived:
    """
    Useful preevaluated values with servo
    """
    servoUniqueId = 0
    degRange = 1
    posRange = 1
    msPerPos = 1

    def updateValues(self, servoStatic, servoType):
        self.servoUniqueId = (servoStatic.arduinoIndex * 100) + servoStatic.pin
        self.degRange = servoStatic.maxDeg - servoStatic.minDeg
        self.posRange = servoStatic.maxPos - servoStatic.minPos

        # a servo has normally a shaft rotation speed for a 60° swipe defined
        # this is the maximum speed possible by the servo
        # the inmoov robot has in many cases not a direct shaft connection for a movement
        # but a mechnical gear mechanism in between
        # for these servos we can define a max move speed of the controlled part
        # msPerPos uses the move speed if it is slower than the servo speed
        # robotControl checks requested move durations against the max speed possible and
        # increases move duration if necessary
        # ATTENTION: servoStatic.moveSpeed is ms/60 deg, servoTypeSpeed is s/60 deg,
        if (servoStatic.moveSpeed / 1000) > servoType.typeSpeed:
            self.msPerPos = servoStatic.moveSpeed / 60
        else:
            self.msPerPos = servoType.typeSpeed * 1000 / 60


# part of dict with key servoName
@dataclass
class ServoCurrent:
    #degrees:int = 0
    millisAfterMoveStart:int = 0
    currentPosition:int = 0         # the requested (non-feedback servo) or measured position
    requestedPosition:int = 0       # the target position for a move
    servoWritePosition:int = 0      # the position written to the servo
    wantedPosition:int = 0          # the linear progress position within the move
    assigned:bool = False
    moving:bool = False
    attached:bool = False
    autoDetach:int = 0
    verbose:bool = False
    swiping:bool = False
    inRequestList:bool = False
    timeOfLastMoveRequest:float = 0.0

    def updateValues(self, newValues):
        #self.degrees = newValues['degrees']
        self.millisAfterMoveStart = newValues['millisAfterMoveStart']
        self.currentPosition = newValues['currentPosition']
        self.requestedPosition = newValues['requestedPosition']
        self.servoWritePosition = newValues['servoWritePosition']
        self.wantedPosition = newValues['wantedPosition']
        self.assigned = newValues['assigned']
        self.moving = newValues['moving']
        self.attached = newValues['attached']
        self.autoDetach = newValues['autoDetach']
        self.verbose = newValues['verbose']
        self.swiping = newValues['swiping']
        self.inRequestList = newValues['inRequestList']
        self.timeOfLastMoveRequest = newValues['timeOfLastMoveRequest']

    def updatePositionOnly(self, position):
        self.expectedPosition = newValues['position']