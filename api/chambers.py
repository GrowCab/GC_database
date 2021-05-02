from time import sleep

from flask.views import MethodView
from flask_smorest import Blueprint

from models.models import Chamber, ChamberSensor, ChamberSchema, Unit, SensorUnit, Sensor, UnitSchema, \
    SensorUnitSchema, SensorMeasure, MeasureSchema

chamber_blp = Blueprint('chambers', 'chambers',
                        url_prefix='/api',
                        description='Operations on Chambers')


def get_chamber_units(chamber_id):
    return Unit.query.join(SensorUnit.sensor).join(Sensor.chamber_sensor). \
        filter(ChamberSensor.chamber_id == chamber_id).all()


def get_chamber_sensor(chamber_id):
    return SensorUnit.query.join(ChamberSensor.sensor).filter(ChamberSensor.chamber_id == chamber_id).all()


@chamber_blp.route('/chambers')
class ChambersList(MethodView):
    @chamber_blp.doc(operationId='getChambers')
    @chamber_blp.response(200, ChamberSchema(many=True))
    def get(self):
        """Get the list of configurations

        -------------------
        :return: Returns a list of configurations objects
        """
        return Chamber.query.all()


@chamber_blp.route('/chamber/<int:chamber_id>')
class ChamberAPI(MethodView):
    @chamber_blp.doc(operationId='getChamber')
    @chamber_blp.response(200, ChamberSchema)
    def get(self, chamber_id):
        """Get the chamber and related objects
        :param chamber_id: ID of the chamber
        :return: Returns a Chamber object
        """
        return Chamber.query.join(ChamberSensor.chamber).filter(Chamber.id == chamber_id).one_or_none()


@chamber_blp.route('/chamber_sensors/<int:chamber_id>')
class ChamberSensorAPI(MethodView):
    @chamber_blp.doc(operationId='getChamberSensors')
    @chamber_blp.response(200, SensorUnitSchema(many=True))
    def get(self, chamber_id):
        """Get the sensors for a chamber
        :param chamber_id:
        :return:
        """
        return get_chamber_sensor(chamber_id)


@chamber_blp.route('/chamber_units/<int:chamber_id>')
class ChamberUnitsAPI(MethodView):
    @chamber_blp.doc(operationId='getChamberUnits')
    @chamber_blp.response(200, UnitSchema(many=True))
    def get(self, chamber_id):
        """Get the units available for this chamber

        This is useful for understanding which dials to present but also which values to use for filtering/separating
        the ExpectedMeasure(s) of a Configuration for a Chamber
        :param chamber_id: ID of the chamber
        :return: Returns a list of Unit objects
        """
        return get_chamber_units(chamber_id)


@chamber_blp.route('/chamber_status/<int:chamber_id>')
class ChamberMeasureAPI(MethodView):
    @chamber_blp.doc(operationId='getChamberStatus')
    @chamber_blp.response(200, MeasureSchema(many=True))
    def get(self, chamber_id):
        # sleep(1)
        results = SensorMeasure.query.join(ChamberSensor.sensor).filter(ChamberSensor.chamber_id == chamber_id).all()
        return results
