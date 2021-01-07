
import numpy as np
from dataclasses import dataclass

import marvinglobal.marvinglobal as mg

###########################################
# cart data classes
###########################################
@dataclass
class State:
    cartStatus:mg.CartStatus = mg.CartStatus.UNKNOWN
    cartMoving:bool = False
    cartRotating:bool = False
    Voltage12V:float = 12
    currentCommand:str = "STOP"
    cartDocked:bool = False


@dataclass
class ImuData:
    yaw:float = 0
    roll:float = 0
    pitch:float = 0
    yawCorrection:float = 0
    updateTime:float = 0

# use SetModifiedFlagOnChange as base class
@dataclass
class Location:
    x:float = 0
    y:float = 0
    yaw:float = 999     # trigger initial location message
    lastLocationSaveTime:float = 0


# use SetModifiedFlagOnChange as base class
@dataclass
class Movement:
    # can not use subclasses as they get not transferred through queue
    #start = Location()
    #target = Location()
    startX = 0
    startY = 0
    startYaw = 0
    targetX = 0
    targetY = 0
    targetYaw = 0

    moveDirection = None    # this is the enum moveDirection value, not an angle
    moveAngle = 0               # this is the angle the cart is moving

    distanceRequested = 0
    distanceMoved = 0
    protected = False

    rotationRequested = 0
    rotationDirection  = mg.MoveDirection.ROTATE_LEFT
    rotated = 0

    moveStartTime = None
    maxDuration: float = None

    obstacleFromUltrasonicDistanceSensor = 0
    obstacleFromInfraredDistanceSensor = 0
    sensorIdObstacle = None
    abyssFromInfraredDistanceSensor = 0
    sensorIdAbyss = None

    blocked:bool = False
    blockedStartTime:float = None

    #currentCommand:str = "STOP"    use state for currentCommand
    reasonStopped:str = ""

    def evalMoveAngle(self, moveDirection):
        # returns the angle of the move based on current yaw and move direction
        directionAngle = {
            mg.MoveDirection.STOP: None,
            mg.MoveDirection.FORWARD: 0,
            mg.MoveDirection.BACKWARD: 180,
            mg.MoveDirection.LEFT: 90,
            mg.MoveDirection.RIGHT: -90,
            mg.MoveDirection.FOR_DIAG_LEFT: 45,
            mg.MoveDirection.FOR_DIAG_RIGHT: -45,
            mg.MoveDirection.BACK_DIAG_LEFT: 135,
            mg.MoveDirection.BACK_DIAG_RIGHT: -135}[moveDirection]

        move360 = (self.startYaw + directionAngle) % 360
        if move360 > 180:
            move360 -= 360
        return move360


@dataclass
class SensorTestData:
    sensorId:int = 0
    distance:np.ndarray = np.zeros((mg.NUM_SCAN_STEPS), dtype=np.int16)
    numMeasures:int = 0
    sumMeasures:np.ndarray = np.zeros((mg.NUM_SCAN_STEPS), dtype=np.int16)


#@dataclass do not use dataclass as it has side effects when setting values
class IrSensorReferenceDistance:
    def __init__(self):
        self.distances:np.ndarray = np.zeros((mg.NUM_SCAN_STEPS), dtype=np.int16)


#@dataclass do not use dataclass as it has side effects when setting values
class FloorOffset:
    def __init__(self):
        self.obstacleHeight:np.ndarray = np.zeros((mg.NUM_SCAN_STEPS), dtype=np.int16)
        self.abyssDepth:np.ndarray = np.zeros((mg.NUM_SCAN_STEPS), dtype=np.int16)
        self.lastUpdate:float = 1.0      # causes sensor to be drawn on init


@dataclass
class ObstacleDistance:
    distance = np.zeros((mg.NUM_US_DISTANCE_SENSORS), dtype=np.int16)
    timeStamp = np.zeros((mg.NUM_IR_DISTANCE_SENSORS), dtype=np.float)


class Battery:
    def __init__(self, minVoltage):
        self.measureTime:float = None
        self.voltage:float = None
        self.warningLevel:int = minVoltage
