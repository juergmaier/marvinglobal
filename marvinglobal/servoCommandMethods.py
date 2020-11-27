



class ServoCommandMethods:        # use config.sc to access these methods

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
