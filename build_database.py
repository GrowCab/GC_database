import os
from datetime import datetime

from config.config import db
from models.models import Sensor, Chamber, Unit, SensorUnit, Configuration, ExpectedMeasure, ChamberSensor, Measure

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

    temperature_and_humidity_sensor = Sensor(description="BME280")
    illumination_sensor = Sensor(description="ILUM")
    db.session.bulk_save_objects([temperature_and_humidity_sensor, illumination_sensor], return_defaults=True)

    # Add sensor units

    celsius_unit = SensorUnit(min=-30, max=90, unit_id=cel.id, sensor_id=temperature_and_humidity_sensor.id)
    humidity_unit = SensorUnit(min=0, max=100, unit_id=hum.id, sensor_id=temperature_and_humidity_sensor.id)
    lux_unit = SensorUnit(min=0, max=10000, unit_id=lux.id, sensor_id=illumination_sensor.id)
    db.session.bulk_save_objects([celsius_unit, humidity_unit, lux_unit], return_defaults=True)
    db.session.commit()

    # Add sensors to the chamber
    chamber_sensor1 = ChamberSensor(chamber_id=chamber1.id, sensor_id=temperature_and_humidity_sensor.id)
    chamber_sensor2 = ChamberSensor(chamber_id=chamber1.id, sensor_id=illumination_sensor.id)
    db.session.bulk_save_objects([
        chamber_sensor1,
        chamber_sensor2
    ], return_defaults=True)

    # Add a configuration to the chamber

    chamber1_configuration = Configuration(chamber=chamber1, description="Until forever")
    db.session.add(chamber1_configuration)
    db.session.commit()

    expected1 = ExpectedMeasure(expected_value=28, end_hour=6, end_minute=0,
                                configuration=chamber1_configuration, unit=cel)
    expected2 = ExpectedMeasure(expected_value=16, end_hour=23, end_minute=59,
                                configuration=chamber1_configuration, unit=cel)
    db.session.add(expected1)
    db.session.add(expected2)
    db.session.commit()

    db.session.bulk_save_objects([
        ExpectedMeasure(expected_value=0, end_hour=6, end_minute=0, configuration=chamber1_configuration, unit=lux),
        ExpectedMeasure(expected_value=1, end_hour=23, end_minute=59, configuration=chamber1_configuration, unit=lux),
        ExpectedMeasure(expected_value=50, end_hour=23, end_minute=59, configuration=chamber1_configuration, unit=hum)
    ], return_defaults=True)
    db.session.commit()

    all_sensors = Sensor.query.all()
    all_chambers = Chamber.query.all()
    all_sensor_units = SensorUnit.query.all()
    all_units = Unit.query.all()
    all_configurations = Configuration.query.all()

    db.session.bulk_save_objects([
        Measure(sensor_unit_id=humidity_unit.id, chamber_sensor_id=chamber_sensor1.id, current_value=30),
        Measure(sensor_unit_id=lux_unit.id, chamber_sensor_id=chamber_sensor2.id, current_value=1),
        Measure(sensor_unit_id=celsius_unit.id, chamber_sensor_id=chamber_sensor1.id, current_value=20)
    ], return_defaults=True)
    db.session.commit()

    [print(s) for s in all_sensors]
