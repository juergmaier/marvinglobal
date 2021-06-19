
import numpy as np
import marvinglobal.marvinglobal as mg


class CartCommandMethods:

    @staticmethod
    def testSensor(requestQueue, sender, sensorId):
        #print(f"sensor test command added to {requestQueue}")
        requestQueue.put({'sender': sender, 'msgType': mg.CartCommands.TEST_IR_SENSOR, 'sensorId': sensorId})

    @staticmethod
    def move(requestQueue, sender, direction:mg.MoveDirection, speed, distance, protected:bool = True):
        requestQueue.put({'sender': sender, 'msgType': mg.CartCommands.MOVE, 'direction': direction, 'speed': speed, 'distance': distance, 'protected': protected})

    @staticmethod
    def rotate(requestQueue, sender, relAngle: int, speed):
        requestQueue.put({'sender': sender, 'msgType': mg.CartCommands.ROTATE, 'relAngle': relAngle, 'speed': speed})

    @staticmethod
    def setIrSensorReferenceDistances(requestQueue, sender, sensorId:int, distances:np.ndarray):
        requestQueue.put({'sender': sender, 'msgType': mg.CartCommands.SET_IR_SENSOR_REFERENCE_DISTANCES, 'sensorId': sensorId, 'distances': distances})

    @staticmethod
    def setVerbose(requestQueue, sender, verbose:bool):
        requestQueue.put({'sender': sender, 'msgType': mg.CartCommands.SET_VERBOSE, 'flag': verbose})

    @staticmethod
    def stopCart(requestQueue, sender, reason:str):
        requestQueue.put({'sender': sender, 'msgType': mg.CartCommands.STOP_CART, 'reason': reason})
