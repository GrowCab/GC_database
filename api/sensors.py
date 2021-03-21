"""
This is the sensors module and supports all the REST actions for the sensor data
"""
from flask import make_response, abort
from flask.views import MethodView
from flask_smorest import Blueprint

from config import db
from models.models import Sensor, SensorSchema

sensors_blp = Blueprint('sensors', 'sensors', url_prefix='/sensors', description='Operations on sensors')


@sensors_blp.route('/')
class SensorListAPI(MethodView):
    @sensors_blp.response(200, SensorSchema(many=True))
    def get(self):
        """Get the list of sensors

        -------------------
        :return: Returns a list of sensor objects
        """
        return Sensor.query.order_by(Sensor.description).all()

    @sensors_blp.arguments(SensorSchema(partial=True))
    @sensors_blp.response(200, SensorSchema)
    def put(self, sensor):
        """Stores a new sensor

        Each sensor contains an id, description and insertion timestamp
        --------------------------
        :param sensor: A partial sensor object for insertion in the database
        :return:
        Returns the inserted sensor object
        """
        description = sensor.description
        existing_sensor = Sensor.query.filter(Sensor.description == description).one_or_none()

        # Can we insert this sensor?
        if existing_sensor is None:
            # Add the passed in sensor to the database
            db.session.add(sensor)
            db.session.commit()

            return sensor, 201
        else:
            abort(
                409,
                f"Sensor {description} exists already",
            )


sensor_blp = Blueprint('sensor', 'sensor',  url_prefix='/sensor', description='Operations on a single sensor')


@sensor_blp.route('/<int:sensor_id>')
class SensorAPI(MethodView):
    @sensor_blp.response(200, SensorSchema)
    def get(self, sensor_id):
        sensor = Sensor.query.filter(Sensor.id == sensor_id).one_or_none()
        if sensor is not None:
            return sensor
        else:
            abort(404,
                  f"No sensor with ID {sensor_id} was found")

    @sensor_blp.arguments(SensorSchema)
    @sensor_blp.response(200, SensorSchema)
    def put(self, sensor: SensorSchema, sensor_id: int):
        # Get the sensor requested from the db into session
        update_sensor = Sensor.query.filter(Sensor.id == sensor_id).one_or_none()
        # Try to find an existing sensor with the same name as the update
        description = sensor.description

        existing_sensor = Sensor.query.filter(Sensor.description == description).one_or_none()

        # Are we trying to find a sensor that does not exist?
        if update_sensor is None:
            abort(
                404,
                f"Sensor not found for Id: {sensor_id}",
            )

        # Would our update create a duplicate of another sensor already existing?
        elif existing_sensor is not None and existing_sensor.id != sensor_id:
            abort(
                409,
                f"Sensor {description} exists already",
            )

        # Otherwise go ahead and update!
        else:
            # Set the id to the sensor we want to update
            sensor.sensor_id = update_sensor.id

            # merge the new object into the old and commit it to the db
            db.session.merge(sensor)
            db.session.commit()

            return sensor, 200

    def delete(self, sensor_id: int):
        # Get the sensor requested
        sensor = Sensor.query.filter(Sensor.id == sensor_id).one_or_none()

        # Did we find a sensor?
        if sensor is not None:
            db.session.delete(sensor)
            db.session.commit()
            return make_response(
                f"Sensor {sensor_id} deleted", 200
            )

        # Otherwise, nope, didn't find that sensor
        else:
            abort(
                404,
                f"Sensor not found for Id: {sensor_id}",
            )
