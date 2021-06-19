

from marvinglobal import marvinglobal as mg

class SkeletonCommandMethods:        # use config.sc to access these methods

    @staticmethod
    def assign(requestQueue, sender, servoName, initialPosition):
        requestQueue.put({'sender': sender, 'msgType': 'assign', 'servoName': servoName, 'position': initialPosition})

    @staticmethod
    def stop(requestQueue, sender, servoName):
        requestQueue.put({'sender': sender, 'msgType': 'stop', 'servoName': servoName})

    @staticmethod
    def positionServo(requestQueue, sender, servoName, position, duration, sequential=True):
        requestQueue.put({'sender': sender, 'msgType': 'position', 'servoName': servoName, 'position': position, 'duration': duration, 'sequential': sequential})

    @staticmethod
    def requestDegrees(requestQueue, sender, servoName, degrees, duration, sequential=True):
        requestQueue.put({'sender': sender, 'msgType': 'requestDegrees', 'servoName': servoName, 'degrees': degrees, 'duration': duration, 'sequential': sequential})

    @staticmethod
    #def setVerbose(requestQueue, sender, servoName, verbose):
    def setVerbose(requestQueue, sender:str, servoName:str, verboseState:bool):
        requestQueue.put({'sender': sender, 'msgType': 'requestVerboseState', 'servoName': servoName, 'verboseOn': verboseState})

    @staticmethod
    def allServoStop(requestQueue, sender):
        requestQueue.put({'sender': sender, 'msgType': 'allServoStop'})

    @staticmethod
    def allServoRest(requestQueue, sender):
        requestQueue.put({'sender':sender, 'msgType': 'allServoRest'})

    @staticmethod
    def setAutoDetach(requestQueue, sender, servoName, duration):
        requestQueue.put({'sender': sender, 'msgType': 'setAutoDetach', 'servoName': servoName, 'duration': duration})


    @staticmethod
    def startRandomMoves(requestQueue, sender):
        requestQueue.put({'sender': sender, 'msgType': 'startRandomMoves'})

    @staticmethod
    def stopRandomMoves(requestQueue, sender):
        requestQueue.put({'sender': sender, 'msgType': 'stopRandomMoves'})


    @staticmethod
    def startSwipe(requestQueue, sender, servoName):
        requestQueue.put({'sender': sender, 'msgType': 'startSwipe', 'servoName': servoName})

    @staticmethod
    def stopSwipe(requestQueue, sender, servoName):
        requestQueue.put({'sender': sender, 'msgType': 'stopSwipe', 'servoName': servoName})


    @staticmethod
    def startGesture(requestQueue, sender, gesture):
        requestQueue.put({'sender': sender, 'msgType': 'startGesture', 'gesture': gesture})

    @staticmethod
    def stopGesture(requestQueue, sender):
        requestQueue.put({'sender': sender, 'msgType': 'stopGesture'})

