Global Constances and Classes used throughout InMoov processes to be used to share data between marvin processes
use

pip install -e d:\projekte\inmoov\marvinglobal
to make it importable

then use

- import marvinglobal.marvinglobal as mg
- import marvinglobal.servoClasses as servoCls

in the program

````puml
@startuml
class CartCommandMethods {
    + testSensor (requestQueue, sensorId)
    --
    + move (requestQueue, direction:int, speed, distance, protected:bool = True)
    --
    + rotate (requestQueue, relAngle: int, speed)
    --
    + setIrSensorReferenceDistances (requestQueue, sensorId:int, distances:np.ndarray)
    --
    + setVerbose (requestQueue, verbose:bool)
    }
@enduml
````
