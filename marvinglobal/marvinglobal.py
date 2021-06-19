
import sys
import time, datetime
import numpy as np
from multiprocessing.managers import SyncManager
import subprocess
from enum import Enum, auto
from dataclasses import dataclass, field

#from marvinglobal import environmentClasses

import marvinglobal.usedSharedRessources as usr

SHARED_DATA_PORT = 50000

SERVO_TYPE_DEFINITIONS_FILE = '/home/marvin/InMoov//marvinData/servoTypeDefinitions.json'
SERVO_STATIC_DEFINITIONS_FILE = '/home/marvin/InMoov/marvinData/servoStaticDefinitions.json'
SERVO_FEEDBACK_DEFINITIONS_FILE = '/home/marvin/InMoov/marvinData/servoFeedbackDefinitions.json'
PERSISTED_SERVO_POSITIONS_FILE = '/home/marvin/InMoov//marvinData/persistedServoPositions.json'

INMOOV_BASE_FOLDER = '/home/marvin/InMoov'
PERSISTED_DATA_FOLDER = f'{INMOOV_BASE_FOLDER}/marvinData'
ROOM_FOLDER = 'rooms'


class SharedDataItems(Enum):
    PROCESS = 10
    START_ALL_PROCESSES = 11
    ARDUINO = 20
    SERVO_TYPE = 30
    SERVO_STATIC = 31
    SERVO_FEEDBACK = 32
    SERVO_DERIVED = 33
    SERVO_CURRENT = 34
    CART_STATE = 40
    CART_LOCATION = 41
    CART_MOVEMENT = 42
    CART_CONFIGURATION = 43
    CART_TARGET = 44
    FLOOR_OFFSET = 50
    SENSOR_TEST_DATA = 51
    IR_SENSOR_REFERENCE_DISTANCE = 52
    ULTRASONIC_SENSORS = 53
    PLATFORM_IMU = 60
    HEAD_IMU = 61
    ENVIRONMENT_ROOM = 70
    ENVIRONMENT_SCAN_LOCATION_LIST = 71
    ENVIRONMENT_MARKER_LIST = 72


logDataUpdates = [SharedDataItems.ARDUINO]

# cart commands
class CartCommands(Enum):
    TEST_IR_SENSOR = 1
    MOVE = 2
    ROTATE = 3
    SET_IR_SENSOR_REFERENCE_DISTANCES = 4
    SET_VERBOSE = 5
    STOP_CART = 6


# skeleton commands
class SkeletonCommands(Enum):
    SET_VERBOSE = 1


class ImageProcessingCommands(Enum):
    TAKE_IMAGE = 1              # cam:, show:bool,showDuration:int (seconds, 0=wait for key)
    CHECK_FOR_ARUCO_CODE = 2    # cam:, [list of markers] [] = any
    START_MONITOR_FORWARD_MOVE = 10
    STOP_MONITOR_FORWARD_MOVE = 11


class NavManagerCommands(Enum):
    SCAN_ROOM = auto()
    FULL_SCAN_AT_POSITION = auto()
    ARUCO_CHECK_RESULT = auto()
    TAKE_IMAGE_RESULT = auto()


######################################
# ROBOT DIMENSIOLNS, ALL DISTANCES IN METERS
######################################
cartFrontOffset = 0.55/2+0.05   # distance from cart center to cart front (including docking pole)
cartWidth = 0.46                #

skeletonBaseZ = 0.88       # standard table height (could be dynamic, not fully implemented yet)
skeletonHeight = 0.84      # top of head above baseZ
skeletonNeckZ = 0.63       # neck pitch rotation point above skeletonBaseZ
skeletonNeckY = 0.09       # neck pitch rotation point ahead of cart center
distOffsetCamFromCartFront = 0.1    # meters



# image processing
class CamTypes(Enum):
    EYE_CAM = auto()
    CART_CAM = auto()
    HEAD_CAM = auto()

camProperties = {
    CamTypes.EYE_CAM: {'name': 'eyecam', 'deviceId': 10, 'cols': 640, 'rows': 480, 'fovH': 21, 'fovV': 40, 'rotate': -90, 'numReads': 2},
    CamTypes.CART_CAM: {'name': 'cartcam', 'deviceId': 8, 'cols': 640, 'rows': 480, 'fovH': 60, 'fovV': 60, 'rotate': 0, 'numReads': 2},
    CamTypes.HEAD_CAM: {'name': 'headcam', 'deviceId': None, 'cols': 1920, 'rows': 1080, 'fovH': 69.4, 'fovV': 42.5, 'rotate': 0, 'numReads': 5}}


@dataclass
class Location:
    x:float = field(default=0.0, metadata={'unit': 'meter'})
    y:float = field(default=0.0, metadata={'unit': 'meter'})
    z: float = field(default=0.0, metadata={'unit': 'meter'})
    yaw:float = field(default=0.0, metadata={'unit': 'degrees'})     # trigger initial location message
    pitch:float = field(default=0.0, metadata={'unit': 'degrees'})     # trigger initial location message
    roll:float = field(default=0.0, metadata={'unit': 'degrees'})     # trigger initial location message
    timePersisted:float = field(default=time.time(), metadata={'unit': 'timestamp'})

    def reset(self):
        self.x = 0
        self.y = 0
        self.z = 0
        self.yaw = 0
        self.pitch = 0
        self.roll = 0

    def addLocation(self, other):
        """
        object gets updated,
        if you need the original use
        new = copy.copy(original)
        new.add(other)
        """
        self.x += other.x
        self.y += other.y
        self.z += other.z
        self.yaw = (self.yaw + other.yaw) % 360
        self.pitch = (self.pitch + other.pitch) % 360
        self.roll = (self.roll + other.roll) % 360


# this is a relative location with reference to the bottom center of the cart and with all skeleton servon in rest position
# note that skeleton moves need to be taken into account when using this location
camLocation = {
    CamTypes.EYE_CAM: Location(0.150,0.035,0.880+0.700,0,0,0),
    CamTypes.CART_CAM: Location(0.250,0,0.240,0,0,0,0),
    CamTypes.HEAD_CAM: Location(0.195,0,0.880+0.720,0,0.320,0)}

NUM_CAMS = 3


# Neck positions for the head cam
pitchGroundWatchDegrees = -35   # head.neck
pitchAheadWatchDegrees = -15   # head.neck
pitchWallWatchDegrees = -15


neckAngles = [{"neckAngle": pitchWallWatchDegrees, "cam": CamTypes.HEAD_CAM},
              {"neckAngle": 0, "cam": CamTypes.EYE_CAM},
              {"neckAngle": -20, "cam": CamTypes.EYE_CAM}]

NUM_IR_DISTANCE_SENSORS = 10
NUM_SCAN_STEPS = 11

NUM_US_DISTANCE_SENSORS = 4
MAX_US_DISTANCE = 30


class MoveDirection(Enum):
    STOP = 0
    FORWARD = 1
    FOR_DIAG_RIGHT = 2
    FOR_DIAG_LEFT = 3
    LEFT = 4
    RIGHT = 5
    BACKWARD = 6
    BACK_DIAG_RIGHT = 7
    BACK_DIAG_LEFT = 8
    ROTATE_LEFT = 9
    ROTATE_RIGHT = 10

class CartMoveBlockEvents(Enum):
    FREE_PATH = auto()
    CLOSE_RANGE_OBSTACLE = auto()
    FAR_RANGE_OBSTACLE = auto()
    CLOSE_RANGE_ABYSS = auto()
    FAR_RANGE_ABYSS = auto()

CartStatus = Enum('CartStatus', 'UNKNOWN DOWN CONNECTING READY')

CartGuiUpdateRequest = Enum('CartGuiUpdateRequest', 'SENSOR_TEST_DATA FLOOR_OFFSET')



def log(msg, publish=True):

    logtime = str(datetime.datetime.now())[11:23]
#    logging.info(f"{logtime} - {msg}")
    print(f"{logtime} - {msg}")


def signalCaller(sender, receiver, cmd, message):
    if receiver == "imageProcessing":
        config.sharedData.imageProcessingQueue.put(sender, cmd, message)
    if receiver == "navManager":
        config.sharedData.navManagerRequestQueue.put(sender, cmd, message)


def evalDegFromPos(servoStatic, servoDerived, inPos: int):
    # inPos has to be in the 0..180 range (servo.write() limits this)
    # minPos has to be smaller than maxPos. Inversion is handled in the arduino
    # minDegrees always has to be smaller than maxDegrees
    degPerPos = servoDerived.degRange / servoDerived.posRange
    deltaPos = inPos - servoStatic.zeroDegPos

    degrees = deltaPos * degPerPos
    # print(f"degrees: {degrees}")
    return round(degrees)


def evalPosFromDeg(servoStatic, servoDerived, inDeg):
    """
    a servo has min/max pos and deg defined. The 0 degree pos can be off center.
    :param servoStatic:
    :param inDeg:
    :return:
    """
    posPerDeg = servoDerived.posRange / servoDerived.degRange
    pos = (inDeg * posPerDeg) + servoStatic.zeroDegPos
    return round(pos)

def getIrSensorName(sensorId):
    if sensorId < 10:
        return ["swipeFrontLeft  ",
                "swipeFrontCenter",
                "swipeFrontRight ",
                "swipeBackLeft   ",
                "swipeBackCenter ",
                "swipeBackRight  ",
                "staticLeftFront ",
                "staticRightFront",
                "staticLeftBack  ",
                "staticRightBack "][sensorId]
    else:
        return f"invalid {sensorId=}"

def getUsSensorName(sensorID):
    return ["left", "middleLeft", "middleRight", "Right"][sensorID]
