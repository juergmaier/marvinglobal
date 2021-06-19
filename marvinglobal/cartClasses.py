
import time
import numpy as np
from dataclasses import dataclass, field

import marvinglobal.marvinglobal as mg

###########################################
# cart data classes
###########################################
@dataclass
class Configuration:
    floorMaxObstacle:int = 15
    floorMaxAbyss:int = 20
    numRepeatedMeasures = 7
    delayBetweenAnalogReads = 20
    minScanCycleDuration = 80
    finalDockingMoveDistance = 12


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


@dataclass
class Movement:
    startX = 0      # can not use subclasse Location() as they get not transferred through queue?
    startY = 0
    startYaw = 0
    targetX = 0
    targetY = 0
    targetYaw = 0

    moveDirectionEnum = None    # this is the enum moveDirection value, not an angle
    moveAngle = 0               # this is the angle the cart is moving

    distanceRequested = 0
    distanceMoved = 0
    protected = False

    relAngleRequested = 0
    relAngleRotated = 0

    moveStartTime = None
    maxDuration: float = None

    obstacleDistanceHeadcam = None
    obstacleHeightHeadcam = None
    obstacleDistanceUsSensor = None
    obstacleHeightIrSensor = None
    irSensorIdObstacle = None

    abyssDistanceHeadcam = None
    abyssDepthHeadcam = None
    abyssDistanceIrSensor = None
    abyssDepthIrSensor = None
    sensorIdAbyss = None

    blocked:bool = False
    blockedStartTime:float = None
    blockEvent = mg.CartMoveBlockEvents.FREE_PATH

    reasonStopped:str = ""

    def clearBlocking(self):
        self.blocked = False
        self.blockEvent = mg.CartMoveBlockEvents.FREE_PATH
        self.obstacleHeightIrSensor = None
        self.irSensorIdObstacle =  None
        self.usSensorIdObstacle = None
        self.abyssDepthIrSensor = None
        self.irSensorIdAbyss = None
        self.blockedStartTime = None

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
    numMeasures:np.ndarray = np.zeros((mg.NUM_SCAN_STEPS), dtype=np.int8)
    sumMeasures:np.ndarray = np.zeros((mg.NUM_SCAN_STEPS), dtype=np.int16)


#@dataclass do not use dataclass as it has side effects when setting values
class IrSensorReferenceDistance:
    def __init__(self):
        self.distances:np.ndarray = np.zeros((mg.NUM_SCAN_STEPS), dtype=np.int16)

class UsSensorDistance:
    def __init__(self):
        self.distance:np.ndarray = np.zeros((mg.NUM_US_DISTANCE_SENSORS), dtype=np.int16)

#@dataclass do not use dataclass as it has side effects when setting values
class FloorOffset:
    def __init__(self):
        self.obstacleHeight:np.ndarray = np.zeros((mg.NUM_SCAN_STEPS), dtype=np.int16)
        self.abyssDepth:np.ndarray = np.zeros((mg.NUM_SCAN_STEPS), dtype=np.int16)
        self.lastUpdate:float = 1.0      # causes sensor to be drawn on init


class Battery:
    def __init__(self, minVoltage):
        self.measureTime:float = None
        self.voltage:float = None
        self.warningLevel:int = minVoltage
