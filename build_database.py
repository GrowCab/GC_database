import os
from config import db
from models.models import Sensor, Configuration, Chamber, Unit, SensorUnit

if __name__ == "__main__":

    # Delete database file if it exists currently
    if os.path.exists("growcab.db"):
        os.remove("growcab.db")

    # Create the database
    db.create_all()

    # populate the database

    # Add a new example chamber

    db.session.add(Chamber(description="Example"))
    db.session.commit()

    # Add units

    lux = Unit(description='lux')
    hum = Unit(description='hum')
    cel = Unit(description='C')

    db.session.bulk_save_objects([lux, hum, cel])
    db.session.commit()

    # Add a new sensor

    temperature_and_humidity_sensor = Sensor(description="BME280", chamber_id=1)
    illumination_sensor = Sensor(description="ILUM", chamber_id=1)
    db.session.bulk_save_objects([temperature_and_humidity_sensor, illumination_sensor])

    # Add sensor units

    celsius_unit = SensorUnit(min=-30, max=90, unit_id=3, sensor_id=1)
    humidity_unit = SensorUnit(min=0, max=100, unit_id=2, sensor_id=1)
    lux_unit = SensorUnit(min=0, max=10000, unit_id=1, sensor_id=2)
    db.session.bulk_save_objects([celsius_unit, humidity_unit, lux_unit])
    db.session.commit()

    all_sensors = Sensor.query.all()
    all_chambers = Chamber.query.all()
    all_sensor_units = SensorUnit.query.all()
    all_units = Unit.query.all()
    [print(s) for s in all_sensors]
