
import time, datetime
from multiprocessing.managers import SyncManager

class ShareManager(SyncManager): pass

def log(msg, publish=True):

    logtime = str(datetime.datetime.now())[11:23]
#    logging.info(f"{logtime} - {msg}")
    print(f"{logtime} - {msg}")


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
    """
    cServoCurrent:  the current status and position of the servo
        servoName
        assigned
        moving
        attached
        autoDetach
        verbose
        position
        degrees
        timeOfLastMoveRequest
    """

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


class ServoCommands:        # use config.sc to access these methods

    @staticmethod
    def assign(requestQueue, servoName, initialPosition):
        requestQueue.put({'cmd': 'assign', 'servoName': servoName, 'position': initialPosition})

    @staticmethod
    def stop(requestQueue, servoName):
        requestQueue.put({'cmd': 'stop', 'servoName': servoName})

    @staticmethod
    def positionServo(requestQueue, servoName, position, duration):
        requestQueue.put({'cmd': 'position', 'servoName': servoName, 'position': position, 'duration': duration})

    @staticmethod
    def setVerbose(requestQueue, servoName, verbose):
        requestQueue.put({'cmd': 'setVerbose', 'servoName': servoName, 'verbose': verbose})

    @staticmethod
    def allServoStop(requestQueue):
        requestQueue.put({'cmd': 'allServoStop'})

    @staticmethod
    def allServoRest(requestQueue):
        requestQueue.put({'cmd': 'allServoRest'})

    @staticmethod
    def setAutoDetach(requestQueue, servoName, duration):
        requestQueue.put({'cmd': 'setAutoDetach', 'servoName': servoName, 'duration': duration})


    @staticmethod
    def startRandomMoves(requestQueue):
        requestQueue.put({'cmd': 'startRandomMoves'})

    @staticmethod
    def stopRandomMoves(requestQueue):
        requestQueue.put({'cmd': 'stopRandomMoves'})


    @staticmethod
    def startSwipe(requestQueue, servoName):
        requestQueue.put({'cmd': 'startSwipe', 'servoName': servoName})

    @staticmethod
    def stopSwipe(requestQueue, servoName):
        requestQueue.put({'cmd': 'stopSwipe', 'servoName': servoName})


    @staticmethod
    def startGesture(requestQueue, gesture):
        requestQueue.put({'cmd': 'startGesture', 'gesture': gesture})

    @staticmethod
    def stopGesture(requestQueue):
        requestQueue.put({'cmd': 'stopGesture'})


class MarvinGlobal:

    def __init__(self):

        # register share functions
        log(f"connect with marvinData")
        ShareManager.register('getProcessDict')
        ShareManager.register('getArduinoDict')
        ShareManager.register('getServoTypeDict')
        ShareManager.register('getServoStaticDict')
        ShareManager.register('getServoDerivedDict')
        ShareManager.register('getServoCurrentDict')

        ShareManager.register('getDictUpdateQueue')
        ShareManager.register('getGuiUpdateQueue')
        ShareManager.register('getServoRequestQueue')
        ShareManager.register('getSpeakRequestQueue')
        ShareManager.register('getSpeakRespondQueue')
        ShareManager.register('getImageProcessingQueue')

    def connect(self):

        # connect with marviData process
        m = ShareManager(address=('127.0.0.1', 50000), authkey=b'marvin')

        try:
            m.connect()
        except Exception as e:
            log(f"could not connect with marvinData, {e}")
            return False

        try:
            self.processDict = m.getProcessDict()

            log(f"processDict available")
        except Exception as e:
            log(f"could not get access to processDict, {e}")
            return False

        try:
            self.arduinoDict = m.getArduinoDict()
            log(f"arduinoDict available")
        except Exception as e:
            log(f"could not get access to arduinoDict, {e}")
            return False

        try:
            self.servoTypeDict = m.getServoTypeDict()
            log(f"servoTypeDict available")
            #log(self.servoTypeDict.get('MG996R').typeMaxPos)
        except Exception as e:
            log(f"could not get access to servoTypeDict, {e}")
            return False

        try:
            self.servoStaticDict = m.getServoStaticDict()
            log(f"servoStaticDict available")
        except Exception as e:
            log(f"could not get access to servoStaticDict, {e}")
            return False

        try:
            self.servoDerivedDict = m.getServoDerivedDict()
            log(f"servoDerivedDict available")
        except Exception as e:
            log(f"could not get access to servoDerivedDict, {e}")
            return False

        try:
            self.servoCurrentDict = m.getServoCurrentDict()
            log(f"servoCurrentDict available")
        except Exception as e:
            log(f"could not get access to servoCurrentDict, {e}")
            return False

        try:
            self.dictUpdateQueue = m.getDictUpdateQueue()
            log(f"dictUpdateQueue available")
        except Exception as e:
            log(f"could not get access to dictUpdateQueue, {e}")
            return False

        try:
            self.guiUpdateQueue = m.getGuiUpdateQueue()
            log(f"guiUpdateQueue available")
        except Exception as e:
            log(f"could not get access to guiUpdateQueue, {e}")
            return False

        try:
            self.servoRequestQueue = m.getServoRequestQueue()
            log(f"servoRequestQueue available")
        except Exception as e:
            log(f"could not get access to servoRequestQueue, {e}")
            return False

        try:
            self.speakRequestQueue = m.getSpeakRequestQueue()
            log(f"speakRequestQueue available")
        except Exception as e:
            log(f"could not get access to speakRequestQueue, {e}")
            return False

        try:
            self.speakRespondQueue = m.getSpeakRespondQueue()
            log(f"speakRespondQueue available")
        except Exception as e:
            log(f"could not get access to speakRespondQueue, {e}")
            return False

        try:
            self.imageProcessingQueue = m.getImageProcessingQueue()
            log(f"imageProcessingQueue available")
        except Exception as e:
            log(f"could not get access to imageProcessingQueue, {e}")
            return False

        return True


    def updateSharedDict(self, cmd):
        try:
            self.dictUpdateQueue.put(cmd)
            return True
        except Exception as e:
            print(f"connection with shared data lost, {e=}")
            return False


    def updateProcessDict(self, processName):
        # need to use the dictUpdateQueue
        cmd = ("processDict", processName, {'lastUpdate': time.time()})
        return self.updateSharedDict(cmd)


    def isProcessRunning(self, processName):
        '''
        each process needs to update the shared process list with the last update time
        '''
        if processName in self.processDict.keys():
            return time.time() - self.processDict.get(processName)['lastUpdate'] > 2
        else:
            return False



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
