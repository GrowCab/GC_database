import os
from datetime import datetime

from config.config import db
from models.models import Sensor, Chamber, Unit, SensorUnit, Configuration, ExpectedMeasure, ChamberSensor, \
    SensorMeasure, \
    MeasureGroup, Actuator, ActuatorEffect, ActuatorMeasure, ChamberActuator

if __name__ == "__main__":

    # Delete database file if it exists currently
    if os.path.exists("growcab.db"):
        os.remove("growcab.db")

    # Create the database
    db.create_all()

    # populate the database

    # Add a new example chamber
    chamber1 = Chamber(description="Example")
    db.session.add(chamber1)
    db.session.commit()

    # Add units

    lux = Unit(description='L')
    hum = Unit(description='%')
    cel = Unit(description='C')

    db.session.bulk_save_objects([lux, hum, cel], return_defaults=True)
    db.session.commit()

    # Add a new sensors
    temperature_and_humidity_sensor = Sensor(description="Temperature", hardware_classname="BME280")
    illumination_sensor = Sensor(description="ILUM", hardware_classname="TSL2561")
    db.session.add_all([temperature_and_humidity_sensor, illumination_sensor])
    db.session.commit()

    # Add sensor units
    celsius_unit = SensorUnit(min=-30, max=90, unit=cel, sensor=temperature_and_humidity_sensor)
    humidity_unit = SensorUnit(min=0, max=100, unit=hum, sensor=temperature_and_humidity_sensor)
    lux_unit = SensorUnit(min=0, max=10000, unit=lux, sensor=illumination_sensor)
    db.session.add_all([celsius_unit, humidity_unit, lux_unit])
    db.session.commit()

    # Add sensors to the chamber
    chamber_sensor1 = ChamberSensor(chamber=chamber1, sensor=temperature_and_humidity_sensor)
    chamber_sensor2 = ChamberSensor(chamber=chamber1, sensor=illumination_sensor)
    db.session.add_all([
        chamber_sensor1,
        chamber_sensor2
    ])
    db.session.commit()

    # Add a configuration to the chamber
    chamber1_configuration = Configuration(chamber_id=chamber1.id, description="Until forever")
    db.session.add(chamber1_configuration)
    db.session.commit()

    expected1 = ExpectedMeasure(expected_value=28, end_hour=6, end_minute=0,
                                configuration=chamber1_configuration, unit=cel)
    expected2 = ExpectedMeasure(expected_value=16, end_hour=23, end_minute=59,
                                configuration=chamber1_configuration, unit=cel)
    db.session.add_all([expected1, expected2])
    db.session.commit()

    db.session.add_all([
        ExpectedMeasure(expected_value=0, end_hour=6, end_minute=0, configuration=chamber1_configuration,
                        unit_id=lux.id),
        ExpectedMeasure(expected_value=1, end_hour=23, end_minute=59, configuration=chamber1_configuration,
                        unit_id=lux.id),
        ExpectedMeasure(expected_value=50, end_hour=23, end_minute=59, configuration=chamber1_configuration,
                        unit_id=hum.id)
    ])
    db.session.commit()

    all_sensors = Sensor.query.all()
    all_chambers = Chamber.query.all()
    all_sensor_units = SensorUnit.query.all()
    all_units = Unit.query.all()
    all_configurations = Configuration.query.all()

    light_actuator = Actuator(description="Light actuator")
    light_actuator.actuator_effect.append(ActuatorEffect(change=1, actuator_id=light_actuator.id, unit_id=lux.id))
    cooling_actuator = Actuator(description="cooling actuator")
    cooling_actuator.actuator_effect.append(ActuatorEffect(change=-10, actuator_id=cooling_actuator.id, unit_id=cel.id))
    heating_actuator = Actuator(description="heating actuator")
    heating_actuator.actuator_effect.append(ActuatorEffect(change=5, actuator_id=heating_actuator.id, unit_id=hum.id))
    humidity_actuator = Actuator(description="humidifier")
    humidity_actuator.actuator_effect.append(ActuatorEffect(change=10, actuator_id=humidity_actuator.id, unit_id=cel.id))

    db.session.add_all([light_actuator, cooling_actuator, heating_actuator, humidity_actuator])
    db.session.commit()

    chamber1_light_actuator = ChamberActuator(chamber=chamber1, actuator=light_actuator)
    db.session.add(chamber1_light_actuator)
    db.session.commit()

    measure_group = MeasureGroup()
    measure_group.sensor_measure.extend([
        SensorMeasure(sensor_unit=humidity_unit, chamber_sensor=chamber_sensor1, current_value=30),
        SensorMeasure(sensor_unit=lux_unit, chamber_sensor=chamber_sensor2, current_value=1),
        SensorMeasure(sensor_unit=celsius_unit, chamber_sensor=chamber_sensor1, current_value=20)
    ])
    measure_group.actuator_measure.extend([
        ActuatorMeasure(chamber_actuator=chamber1_light_actuator, measure_group=measure_group, current_value=0)
    ])
    db.session.add(measure_group)
    db.session.commit()

    [print(s) for s in all_sensors]
