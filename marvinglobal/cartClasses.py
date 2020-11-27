
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

    start = Location()
    target = Location()
    moveDirection = None    # this is the enum moveDirection value, not an angle

    distanceRequested = 0
    distanceMoved = 0
    protected = False

    rotationRequested = 0
    rotationDirection  = mg.MoveDirection.ROTATE_LEFT
    rotated = 0

    moveStartTime = None
    maxDuration: float = None

    obstacleFromUltrasonicDistanceSensor = "-"
    obstacleFromInfraredDistanceSensor = "-"
    sensorIdObstacle = None
    abyssFromInfraredSensor = "-"
    sensorIdAbyss = None

    blocked:bool = False
    blockedStartTime:float = None

    currentCommand:str = "STOP"
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

        return (self.start.yaw + directionAngle) % 360  # make 0 degrees pointing to the right


    def updateCartRotation(self):
        self.rotated = (self.current.yaw - self.start.yaw) % 360

@dataclass
class SensorTestData:
    sensorId:int = 0
    distance:np.ndarray = np.zeros((mg.NUM_SCAN_STEPS), dtype=np.int16)
    numMeasures:int = 0
    sumMeasures:np.ndarray = np.zeros((mg.NUM_SCAN_STEPS), dtype=np.int16)


@dataclass
class IrSensorReferenceDistance:
    distances:np.ndarray = np.zeros((mg.NUM_SCAN_STEPS), dtype=np.int16)


@dataclass
class FloorOffset:
    offset:np.ndarray = np.zeros((mg.NUM_SCAN_STEPS), dtype=np.int16)
    lastUpdate:float = 1.0      # causes sensor to be drawn on init


@dataclass
class ObstacleDistance:
    distance = np.zeros((mg.NUM_US_DISTANCE_SENSORS), dtype=np.int16)
    timeStamp = np.zeros((mg.NUM_IR_DISTANCE_SENSORS), dtype=np.float)


class Battery:
    def __init__(self, minVoltage):
        self.measureTime:float = None
        self.voltage:float = None
        self.warningLevel:int = minVoltage
