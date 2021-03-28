```mermaid
classDiagram

class Sensor{
    +String description
}

class SensorUnit{
    +float precision
    +float min
    +float max
}

class Unit{
    +String description
}

class MeasureGroup{
    +datetime timestamp
}

class Measure{
    +float value
}

class ExpectedMeasure{
    +float expected_value
    +int start_hour
    +int start_minute
    +int end_hour
    +int end_minute
}
class Configuration{
    +datetime start
    +datetime end
    +String description
}
class Chamber{
    +String description
}

class Actuator{
    +String description
}

class ActuatorEffect{
    +int change
}

MeasureGroup --o Measure
Measure -- ChamberSensor
SensorUnit -- Measure
Sensor --o SensorUnit
SensorUnit -- Unit
Chamber --o ChamberSensor
Sensor -- ChamberSensor
ExpectedMeasure -- Unit
Configuration --o ExpectedMeasure
Chamber --o Configuration
Chamber --o Actuator
Actuator --o ActuatorEffect
ActuatorEffect -- Unit

```