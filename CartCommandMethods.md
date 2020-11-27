````puml
@startuml
class CartCommandMethods {
    + testSensor 
    (requestQueue, sensorId)
    + move (requestQueue, direction:int, speed, distance, protected:bool = True)
    + rotate (requestQueue, relAngle: int, speed)
    + setIrSensorReferenceDistances (requestQueue, sensorId:int, distances:np.ndarray)
    + setVerbose (requestQueue, verbose:bool)
    }
@enduml
````
