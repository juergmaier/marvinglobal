

from marvinglobal import marvinglobal as mg

class SkeletonCommandMethods:        # use config.sc to access these methods

    @staticmethod
    def assign(requestQueue, sender, servoName, initialPosition):
        requestQueue.put({'sender': sender, 'cmd': 'assign', 'servoName': servoName, 'position': initialPosition})

    @staticmethod
    def stop(requestQueue, sender, servoName):
        requestQueue.put({'sender': sender, 'cmd': 'stop', 'servoName': servoName})

    @staticmethod
    def positionServo(requestQueue, sender, servoName, position, duration, sequential=True):
        requestQueue.put({'sender': sender, 'cmd': 'position', 'servoName': servoName, 'position': position, 'duration': duration, 'sequential': sequential})

    @staticmethod
    def requestDegrees(requestQueue, sender, servoName, position, duration, sequential=True):
        requestQueue.put({'sender': sender, 'cmd': 'requestDegrees', 'servoName': servoName, 'degrees': position, 'duration': duration, 'sequential': sequential})

    @staticmethod
    #def setVerbose(requestQueue, sender, servoName, verbose):
    def setVerbose(requestQueue, sender, servoName, verboseOn):
        requestQueue.put({'sender': sender, 'cmd': 'setVerbose', 'servoName': servoName, 'verboseOn': verboseOn})

    @staticmethod
    def allServoStop(requestQueue, sender):
        requestQueue.put({'sender': sender, 'cmd': 'allServoStop'})

    @staticmethod
    def allServoRest(requestQueue, sender):
        requestQueue.put({'sender':sender, 'cmd': 'allServoRest'})

    @staticmethod
    def setAutoDetach(requestQueue, sender, servoName, duration):
        requestQueue.put({'sender': sender, 'cmd': 'setAutoDetach', 'servoName': servoName, 'duration': duration})


    @staticmethod
    def startRandomMoves(requestQueue, sender):
        requestQueue.put({'sender': sender, 'cmd': 'startRandomMoves'})

    @staticmethod
    def stopRandomMoves(requestQueue, sender):
        requestQueue.put({'sender': sender, 'cmd': 'stopRandomMoves'})


    @staticmethod
    def startSwipe(requestQueue, sender, servoName):
        requestQueue.put({'sender': sender, 'cmd': 'startSwipe', 'servoName': servoName})

    @staticmethod
    def stopSwipe(requestQueue, sender, servoName):
        requestQueue.put({'sender': sender, 'cmd': 'stopSwipe', 'servoName': servoName})


    @staticmethod
    def startGesture(requestQueue, sender, gesture):
        requestQueue.put({'sender': sender, 'cmd': 'startGesture', 'gesture': gesture})

    @staticmethod
    def stopGesture(requestQueue, sender):
        requestQueue.put({'sender': sender, 'cmd': 'stopGesture'})

