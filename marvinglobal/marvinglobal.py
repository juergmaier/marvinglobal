
import sys
import time, datetime
import numpy as np
from multiprocessing.managers import SyncManager
import subprocess
from enum import Enum
from dataclasses import dataclass

import marvinglobal.usedSharedRessources as usr

SHARED_DATA_PORT = 50000

SERVO_STATIC_DEFINITIONS_FILE = 'd:/projekte/inmoov/marvinData/servoStaticDefinitions.json'
SERVO_TYPE_DEFINITIONS_FILE = 'd:/projekte/inmoov/marvinData/servoTypeDefinitions.json'
PERSISTED_SERVO_POSITIONS_FILE = 'd:/projekte/inmoov/marvinData/persistedServoPositions.json'


class SharedDataItem(Enum):
    PROCESS = 10
    ARDUINO = 20
    SERVO_TYPE = 30
    SERVO_STATIC = 31
    SERVO_DERIVED = 32
    SERVO_CURRENT = 33
    CART_STATE = 40
    CART_LOCATION = 41
    CART_MOVEMENT = 42
    CART_CONFIGURATION = 43
    FLOOR_OFFSET = 50
    SENSOR_TEST_DATA = 51
    IR_SENSOR_REFERENCE_DISTANCE = 52
    OBSTACLE_DISTANCE = 53
    PLATFORM_IMU = 60
    HEAD_IMU = 61

logDataUpdates = [SharedDataItem.ARDUINO]

# cart commands
class CartCommand(Enum):
    TEST_IR_SENSOR = 1
    MOVE = 2
    ROTATE = 3
    SET_IR_SENSOR_REFERENCE_DISTANCES = 4
    SET_VERBOSE = 5
    STOP_CART = 6


# skeleton commands
class SkeletonCommand(Enum):
    SET_VERBOSE = 1


class ImageProcessingCommand(Enum):
    CHECK_FOR_ARUCO_CODE = 1
    #ARUCO_CHECK_RESULT = 2
    START_MONITOR_FORWARD_MOVE = 10
    STOP_MONITOR_FORWARD_MOVE = 11

class NavManagerCommand(Enum):
    NEW_TASK = 1
    ARUCO_CHECK_RESULT = 2

# image processing
EYE_CAM = 1
eyeCamProperties = {'name': 'eyecam', 'deviceId': 1, 'cols': 640, 'rows': 480, 'fovH': 21, 'fovV': 40, 'rotate': -90, 'numReads': 2}
CART_CAM = 2
cartCamProperties = {'name': 'cartcam', 'deviceId': 3, 'cols': 640, 'rows': 480, 'fovH': 60, 'fovV': 60, 'rotate': 0, 'numReads': 2}
D415 = 3
HEAD_CAM = 3
D415CamProperties = {'name': 'headcam', 'deviceId': None, 'cols': 1920, 'rows': 1080, 'fovH': 69.4, 'fovV': 42.5, 'rotate': 0, 'numReads': 5}
NUM_CAMS = 3

# Neck positions for the head cam
pitchGroundWatchDegrees = -35   # head.neck
pitchAheadWatchDegrees = -15   # head.neck
pitchWallWatchDegrees = -15

neckAngles = [{"neckAngle": pitchWallWatchDegrees, "cam": HEAD_CAM},
              {"neckAngle": 0, "cam": EYE_CAM},
              {"neckAngle": -20, "cam": EYE_CAM}]

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
