adf
````puml
@startuml
class CartStatus <enumeration> {
    UNKNOWN = 0
    CONNECTING = 1
    READY = 2
    }
@enduml
````
asdf

````puml
@startuml
class State {
    cartStatus: mg.CartStatus
    cartMoving: bool
    cartRotating: bool
    Voltage12V: float
    currentCommand: str
    cartDocked: bool
    }
@enduml
````

