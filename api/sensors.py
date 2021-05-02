"""
This is the sensors module and supports all the REST actions for the sensor data
"""
from time import sleep

from flask import make_response, abort
from flask.views import MethodView
from flask_smorest import Blueprint

from config.config import db, app
from models.models import Sensor, SensorSchema, EditableSensorSchema

sensors_blp = Blueprint('sensors', 'sensors', url_prefix='/api', description='Operations on sensors')


@sensors_blp.route('/sensors')
class SensorListAPI(MethodView):
    @sensors_blp.doc(operationId="getSensors")
    @sensors_blp.response(200, SensorSchema(many=True))
    def get(self):
        """Get the list of sensors

        ---------

        Doctest setup
        ---------
        >>> app.register_blueprint(sensor_blp)
        >>> db.engine.echo = False  # Make the SQLAlchemy a bit quieter to have empty output in the next line

        Examples / Tests
        --------
        >>> response = app.test_client().get('/api/sensors')
        >>> response.status_code
        200

        -------------------
        :return: Returns a list of sensor objects
        """
        sleep(1)
        return Sensor.query.order_by(Sensor.description).all()

    @sensors_blp.doc(operationId="putSensor")
    @sensors_blp.arguments(EditableSensorSchema)
    @sensors_blp.response(200, SensorSchema)
    def put(self, sensor: Sensor):
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


sensor_blp = Blueprint('sensor', 'sensor',  url_prefix='/api/', description='Operations on a single sensor')


@sensor_blp.route('/sensor/<int:sensor_id>')
class SensorAPI(MethodView):
    @sensors_blp.doc(operationId='getSensor')
    @sensor_blp.response(200, SensorSchema)
    def get(self, sensor_id):
        sensor = Sensor.query.filter(Sensor.id == sensor_id).one_or_none()
        if sensor is not None:
            return sensor
        else:
            abort(404,
                  f"No sensor with ID {sensor_id} was found")

    @sensors_blp.doc(operationId='patchSensor')
    @sensor_blp.arguments(SensorSchema)
    @sensor_blp.response(200, SensorSchema)
    def patch(self, sensor: SensorSchema, sensor_id: int):
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

    @sensors_blp.doc(operationId='deleteSensor')
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
