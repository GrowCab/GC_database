import os
from config import db
from models import Sensor

if __name__ == "__main__":
    # Initial sensor list
    SENSORS = [
        {"description": "Temperature"},
        {"description": "Humidity"},
        {"description": "Illumination"},
    ]

    # Delete database file if it exists currently
    if os.path.exists("growcab.db"):
        os.remove("growcab.db")

    # Create the database
    db.create_all()

    # populate the database
    for sensor in SENSORS:
        s = Sensor(description=sensor.get("description"))
        db.session.add(s)

    db.session.commit()
